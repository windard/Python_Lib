## asyncore

基本的异步 io 处理模块，它是一个异步 socket 的封装。在网络上一次处理多个连接常见的三种解决方案：多线程，多进程，和 异步 IO。

多进程的系统开销比较大，多线程难以管理，会导致同步问题，异步 IO 正在越来越受到欢迎，像 nodejs 就大量使用异步 IO 操作，降低系统开销而且能够获得不错的效果，web 服务器 Nginx 也支持各种 异步 IO 的类型，如 select，poll ，epoll 等。

可惜 windows  下只能使用 select 。

异步 IO 的底层实现就是采用 select 模块，高层次的处理异步 IO 的框架就是 asyncore 和 asynchat ，还有 twisted ，是一个非常强大的 网络编程框架。

其实在 Python 中，对于多连接除了这三种常见的解决方案之外还有 协程，也被称为 微线程。

### 使用 多线程 和 多进程的服务器

多进程

```
# coding=utf-8

from SocketServer import TCPServer, ForkingMixIn, StreamRequestHandler


class Server(ForkingMixIn, TCPServer):
    pass


class Handler(StreamRequestHandler):

    def handle(self):
        addr = self.request.getpeername()
        print('Got connection from', addr)
        self.wfile.write('Thank you for connecting .')

server = Server(('', 8899), Handler)
server.serve_forever()

```

多线程

```
# coding=utf-8

from SocketServer import TCPServer, ThreadingMixIn, StreamRequestHandler


class Server(ThreadingMixIn, TCPServer):
    pass


class Handler(StreamRequestHandler):

    def handle(self):
        addr = self.request.getpeername()
        print('Got connection from', addr)
        self.wfile.write('Thank you for connecting .')

server = Server(('', 8899), Handler)
server.serve_forever()

```

### 使用 基础异步 IO

使用 select

```
# coding=utf-8

import socket
import select

s = socket.socket()

host = socket.gethostname()
port = 1234
s.bind((host, port))

s.listen(5)
inputs = [s]

while True:
    rs, ws, es = select.select(inputs, [], [])
    for r in rs:
        if r is s:
            c, addr = s.accept()
            print('Got connection from', addr)
            inputs.append(c)
        else:
            try:
                data = r.recv(1024)
                disconnected = not data
            except socket.error:
                disconnected = True

            if disconnected:
                print r.getpeername(), 'disconnected .'
                inputs.remove(r)
            else:
                print(data)

```

使用 poll

```
# coding=utf-8

import socket
import select

s = socket.socket()

host = socket.gethostname()
port = 1234

s.bind((host, port))

fdmap = {s.fileno(): s}

s.listen(5)
p = select.poll()
p.register(s)

while True:
    events = p.poll()

    for fd, event in events:
        if fd in fdmap:
            c, addr = s.accept()
            print('Get connection from', addr)
            p.register(c)
            fdmap[c.fileno()] = c
        elif event & select.POLLIN:
            data = fdmap[fd].recv(1024)
            if not data:
                print fdmap[fd].getpeername(), 'disconnected .'
                p.unregister(fd)
                del fdmap[fd]
            else:
                print(data)

```

在 Windows 下无法使用，另外好像还有一点点问题，Telnet 输入无法显示，而且退出的时候也没有显示。

### 使用 Twisted

Twisted 是一个 事件驱动 的 Python 网络框架，功能十分丰富。支持包括 web 服务器, web 客户端, SSH, SMTP, POP3, ICQ, IRC, MSN, DNS 等网络服务。

twisted 的简单服务器

```
# coding=utf-8

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory


class SimpleLogger(Protocol):

    def connectionMade(self):
        print('Got connection from', self.transport.client)

    def connectionLost(self, reason):
        print(self.transport.client, 'disconnected .')

    def dataReceived(self, data):
        print(data)

factory = Factory()
factory.protocol = SimpleLogger

reactor.listenTCP(1234, factory)
reactor.run()

```

或者使用预定义协议 LineReceiver

```
# coding=utf-8

from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver


class SimpleLogger(LineReceiver):

    def connectionMade(self):
        print('Got connection from', self.transport.client)

    def connectionLost(self, reason):
        print(self.transport.client, 'disconnected .')

    def lineReceived(self, line):
        print(line)

factory = Factory()
factory.protocol = SimpleLogger

reactor.listenTCP(1234, factory)
reactor.run()

```

使用预定义的 LineReceiver 实现聊天服务器

```
#!/usr/bin/python
# coding=utf-8
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

class Chat(LineReceiver):
    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = "GETNAME"

    def connectionMade(self):
        self.sendLine("What's your name?")

    def connectionLost(self, reason):
        if self.users.has_key(self.name):
            del self.users[self.name]

    def lineReceived(self, line):
        if self.state == "GETNAME":
            self.handle_GETNAME(line)
        else:
            self.handle_CHAT(line)

    def handle_GETNAME(self, name):
        if self.users.has_key(name):
            self.sendLine("Name taken, please choose another.")
            return
        self.sendLine("Welcome, %s!" % (name,))
        self.name = name
        self.users[name] = self
        self.state = "CHAT"

    def handle_CHAT(self, message):
        message = "<%s> %s" % (self.name, message)
        for name, protocol in self.users.iteritems():
            if protocol != self:
                protocol.sendLine(message)

class ChatFactory(Factory):

    def __init__(self):
        self.users = {}    # maps user names to Chat instances

    def buildProtocol(self, addr):
        return Chat(self.users)

if __name__ == '__main__':
    reactor.listenTCP(8123, ChatFactory())
    reactor.run()

```

还有很多其他的预定义协议，等待你去探索。

### 使用 asyncore

asyncore 已经封装好了 socket 的异步 IO 库，所以我们在使用的时候可以直接操作网络，避免使用 socket， select 等底层库。

asyncore 主要使用的是一个类和一个函数

- `asyncore.dispatcher` 类
- `asyncore.loop` 函数

#### dispatcher 基类

每一个从 dispatcher 继承的类的对象，都可以做一个可用的 socket ，可以是 TCP 或者是 UDP，或者是其他的，与普通 socket 无异。

然后我们在需要处理的地方，重写一些方法即可。

常见的处理方法，需要重写

- `handle_connect` 当 socket 创建一个连接时调用
- `handle_accept` 在本地 socket 与远程建立连接时调用 (被动连接)
- `handle_close` 当 socket 关闭连接时调用
- `handle_read` 在异步循环中检测到 read 时调用
- `handle_write` 在异步循环中检测到 write 时调用
- `handle_error` 当引发一个异常而没有其他处理时调用
- `handle_expt` 当发生一个 OOB 异常时执行此方法

- `writable` 每次在异步循环添加 socket 到写事件列表中调用，默认为 True
- `readable` 每次在异步循环添加 socket 到读事件列表中调用，默认为 True

以下方法与标准 socket 模块相同，只需使用即可

- `create_socket` 创建 socket
- `connect` 连接 socket，接收元组第一个参数为主机地址，第二个参数为端口号
- `accept` 接收一个 socket 连接
- `send` 向远程 socket 发送数据
- `recv` 从远程 socket 接收数据，一个空字符 即表示另一端 socket 已关闭
- `listen` 监听 socket 连接
- `bind` 绑定 socket 连接地址
- `close` 关闭 socket 连接

#### loop 函数

loop 函数是全局函数，而并不是单个 dispatcher 对象的函数。它能够自动检测全局的 dispatcher 实例，每次创建一个 dispatcher 实例都会被加入到默认的 channel 中。所以，在创建的时候就可以指定 channel ，在调用 loop 函数的时候也可以指定 channel。

```
# coding=utf-8

import socket
import asyncore


class http_client(asyncore.dispatcher):

    def __init__(self, host, path):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, 80))
        self.buffer = 'GET %s HTTP/1.0\r\n\r\n' % path

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        print self.recv(8192)

    def writable(self):
        return len(self.buffer) > 0

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]

c = http_client('www.baidu.com', '/')
asyncore.loop()

```

这个函数在收发进行了一次之后，buffer 长度为0，writeable 返回 False，故结束连接，进入 handle_close 方法结束。

在该函数库中除了以上主要一个函数和一个类之外还有其他的几个类

- `asyncore.dispatcher_with_send` 是 dispatcher 的子类，增加了简单的缓存输出能力，在客户端中使用
- `asyncore.file_dispatcher` 是 dispatcher 的子类，封装了文件描述符和文件映射函数
- `asyncore.file_wrapper` 是 dispatcher 的子类，增加了文件包装器。

```
# coding=utf-8

import asyncore
import socket


class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        if data:
            self.send(data)


class EchoServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = EchoHandler(sock)

server = EchoServer('localhost', 8080)
asyncore.loop()

```

虽然 asyncore 已经很强大了，不过 Python 还有一个对其进行扩展的库 asynchat ，可以一试。

使用 asyncore 实现的端口转发

```
# -*- coding: utf-8 -*-

import socket
import asyncore


class Receiver(asyncore.dispatcher):
    def __init__(self, conn):
        asyncore.dispatcher.__init__(self, conn)
        self.from_remote_buffer = b''
        self.to_remote_buffer = b''
        self.sender = None

    def handle_connect(self):
        pass

    def handle_read(self):
        read = self.recv(4096)
        # print '%04i -->'%len(read)
        self.from_remote_buffer += read

    def writable(self):
        return len(self.to_remote_buffer) > 0

    def handle_write(self):
        sent = self.send(self.to_remote_buffer)
        # print '%04i <--'%sent
        self.to_remote_buffer = self.to_remote_buffer[sent:]

    def handle_close(self):
        self.close()
        if self.sender:
            self.sender.close()


class Sender(asyncore.dispatcher):
    def __init__(self, receiver, remoteaddr, remoteport):
        asyncore.dispatcher.__init__(self)
        self.receiver = receiver
        receiver.sender = self
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((remoteaddr, remoteport))

    def handle_connect(self):
        pass

    def handle_read(self):
        read = self.recv(4096)
        # print '<-- %04i'%len(read)
        self.receiver.to_remote_buffer += read

    def writable(self):
        return len(self.receiver.from_remote_buffer) > 0

    def handle_write(self):
        sent = self.send(self.receiver.from_remote_buffer)
        # print '--> %04i'%sent
        self.receiver.from_remote_buffer = self.receiver.from_remote_buffer[sent:]

    def handle_close(self):
        self.close()
        self.receiver.close()


class Forwarder(asyncore.dispatcher):
    def __init__(self, ip, port, remoteip, remoteport, backlog=5):
        asyncore.dispatcher.__init__(self)
        self.remoteip = remoteip
        self.remoteport = remoteport
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((ip, port))
        self.listen(backlog)

    def handle_accept(self):
        conn, addr = self.accept()
        # print '--- Connect --- '
        self.log_info('Connected from %s:%s to %s:%s' % (addr[0], addr[1], self.remoteip, self.remoteport))
        Sender(Receiver(conn), self.remoteip, self.remoteport)

if __name__ == '__main__':
    f = Forwarder('127.0.0.1', 5089, '127.0.0.1', 5002)
    asyncore.loop()

```
