## select

典型的 I/O 多路异步库，如果想要解决 10K 问题，常用的解决思路。在 python3 中也有 select，还有 selectors 作为一个更高级的包装支持。

一般常见的 I/O 多路复用就是 select，poll 等，这些在 select 库中都有支持，其实还是比较基础，在 Linux 上还有 epoll ，在 Mac 上还有 kqueue 。

1. select 是个好东西，可以提供很多的多路复用组件,属于基础库提供
2. selectors 也是个好东西，包装 select 提供更高级的接口使用。
3. 但是，凡是就是怕但是，selectors 只在 python3 中作为基础库提供，在python2 里没有
4. 在 python2 中的 selector 和 selectors 都是李鬼，假的，没用的，骗人的，只有 selectors2 是一个替用品

## 简单使用

简单的 转发代理服务器

```python
# -*- coding: utf-8 -*-

import socket
import select
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
remote_addr = ('127.0.0.1', 5002)


class ProxyServer(object):

    def __init__(self, host='localhost', port=8682, listen=5):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(listen)
        self.input_list = []
        self.channel = {}

    def run_forever(self):
        self.input_list.append(self.server)
        while self.input_list:
            readable, writable, exceptable = select.select(self.input_list, [], [])
            logger.debug("event trigger")
            for sock in readable:
                if sock == self.server:
                    self.on_accept()
                    continue

                # 一次读取，没读完咋整？
                # 会触发多次事件，每次都是数据读取，直到读完全部数据
                data = sock.recv(4096)
                if not data:
                    self.on_close(sock)

                else:
                    self.on_recv(sock, data)

    def on_accept(self):
        remote_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_sock.connect(remote_addr)

        client_sock, client_addr = self.server.accept()
        logger.info("receive connection from: %s:%s", *client_addr)
        self.input_list.append(remote_sock)
        self.input_list.append(client_sock)

        self.channel[client_sock] = remote_sock
        self.channel[remote_sock] = client_sock

    def on_close(self, sock):
        logger.info("sock is disconnected: %s:%s", *sock.getpeername())
        # 最好是同时断开，因为如果是半断开，单向写入的时候会有问题
        remote = self.channel[sock]
        self.input_list.remove(remote)
        del self.channel[remote]
        remote.close()

        self.input_list.remove(sock)
        del self.channel[sock]
        sock.close()

    def on_recv(self, sock, data):
        logger.debug("forward data: %d", len(data))
        self.channel[sock].send(data)


if __name__ == '__main__':
    server = ProxyServer()
    try:
        server.run_forever()
    except KeyboardInterrupt:
        logger.info("Ctrl C - Stopping server")

```

使用 selectors 的实现

```python
# -*- coding: utf-8 -*-

import socket
import logging
import selectors


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
remote_addr = ('127.0.0.1', 5002)
selector = selectors.DefaultSelector()


class ProxyServer(object):
    def __init__(self, host='localhost', port=8682, listen=5):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(listen)
        self.channel = {}

    def run_forever(self):
        selector.register(self.server, selectors.EVENT_READ, self.on_accept)
        while True:
            for key, mask in selector.select():
                logger.debug("event trigger")
                key.data(key.fileobj, mask)

    def on_accept(self, _, event_mask):
        logger.debug("on accept event:%r", event_mask)
        remote_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_sock.connect(remote_addr)

        client_sock, client_addr = self.server.accept()
        logger.info("receive connection from: %s:%s", *client_addr)

        self.channel[client_sock] = remote_sock
        self.channel[remote_sock] = client_sock

        selector.register(client_sock, selectors.EVENT_READ, self.on_recv)
        selector.register(remote_sock, selectors.EVENT_READ, self.on_recv)

    def on_close(self, sock):
        logger.info("sock is disconnected: %s:%s", *sock.getpeername())
        # 最好是同时断开，因为如果是半断开，单向写入的时候会有问题
        remote = self.channel[sock]
        del self.channel[remote]
        remote.close()
        selector.unregister(remote)

        del self.channel[sock]
        sock.close()
        selector.unregister(sock)

    def on_recv(self, sock, event_mask):
        # type: (socket.socket, int) -> None
        logger.debug("on read event:%r", event_mask)

        data = sock.recv(4096)
        if not data:
            return self.on_close(sock)

        logger.debug("forward data: %d", len(data))
        self.channel[sock].send(data)


if __name__ == '__main__':
    server = ProxyServer()
    try:
        server.run_forever()
    except KeyboardInterrupt:
        logger.info("Ctrl C - Stopping server")

```

使用 selectors 实现的 echo 服务器

```python
# -*- coding: utf-8 -*-

import select
import socket
import logging
import selectors

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
selector = selectors.DefaultSelector()
# selector = selectors.SelectSelector()
logger.info("selector actually is:%r", selector)
server_addr = ('127.0.0.1', 5677)


def on_read(event_client, event_mask):
    # type: (socket.socket, int) -> None
    logger.info("on read event:%r", event_mask)
    logger.info("read socket:[%d]%r", id(event_client), event_client)
    # 如果 client socket 已经 close ，就无法调用 getpeername 方法，会报错 OSError: [Errno 22] Invalid argument
    try:
        client_address = event_client.getpeername()
        logger.info("client address:%r", client_address)
    except OSError as e:
        # 已经断开连接
        event_client.close()
        logger.info("client already closed")
        logger.info("recv error:%r", e)
        selector.unregister(event_client)
        return
    # 如果 client socket 已经 close，也无法调用 recv 方法，会报错 ConnectionResetError: [Errno 54] Connection reset by peer
    data = event_client.recv(1024)
    if data:
        logger.info("receive message:%r", data)
        # event_client.send("[echo]".encode("utf-8") + data)
        event_client.sendall(data)
    else:
        logger.info("client close")
        selector.unregister(event_client)
        event_client.close()


def on_accept(event_server, event_mask):
    # type: (socket.socket, int) -> None
    logger.info("on accept event:%r", event_mask)
    client, addr = event_server.accept()
    logger.info("accept:%r", addr)
    # TODO: why?
    client.setblocking(False)
    # client.sendall(b"hello world.")
    selector.register(client, selectors.EVENT_READ, on_read)


if __name__ == '__main__':

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind(server_addr)
    server.listen(5)
    logger.info("server listen on:%r", server_addr)

    selector.register(server, selectors.EVENT_READ, on_accept)

    while True:
        logger.info("waiting for I/O")
        # logger.info("selector:%r", selector._fd_to_key)
        # logger.info("selector:%r", selector.get_map())

        # for key, mask in selector.select(1):
        for key, mask in selector.select():
            key.data(key.fileobj, mask)

```

## 参考链接
[12.4. selectors — I/O 多路复用抽象层](https://learnku.com/docs/pymotw/selectors-io-multiplexing-abstractions/3428)     
[12.5. select — 高效地等待 I/O](https://learnku.com/docs/pymotw/select-wait-for-io-efficiently/3429)      
