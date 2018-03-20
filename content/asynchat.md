## asynchat

asynchat 是一个 asyncore 的扩展库，提供了更为强大的面向行协议的支持，主要是用在聊天室的实现。

这个库也是提供一个用来实现的初始类 `asynchat.asyn_chat`,这个类主要有两个方法，再使用的时候必须重写。

- `asyn_chat.collect_incoming_data` 用来收集数据。
- `asyn_chat.found_terminator` 在数据收集结束后用来处理数据。收集数据结束的标志即接收到数据分隔符。

在收集数据之前，初始化这个类的时候，还需要在初始函数里使用 `asyn_chat.set_terminator` 来设定数据分隔符，默认为空。

发送数据方法是 `asyn_chat.push` ，即相当于 `asyncore.send` 或者 `socket.send` 。

使用 asynchat 实现 HTTP 服务器

```
# -*- coding: utf-8 -*-

import time
import socket
import asynchat
import asyncore
from asyncore import dispatcher

PORT = 8008


class HTTPHeaders(dict):
    def getheader(self, key):
        return self.get(key)


class HTTPHandler(asynchat.async_chat):
    def __init__(self, sock, addr):
        asynchat.async_chat.__init__(self, sock=sock)
        self.addr = addr
        self.ibuffer = []
        self.obuffer = ""
        self.set_terminator(b'\r\n\r\n')
        self.reading_headers = True
        self.handling = False
        self.cgi_data = None

    def parse_headers(self, data):
        headers_lines = data.split('\r\n')
        self.request_method, self.path, self.request_version = headers_lines[0].split()
        self.headers = HTTPHeaders(header.split(': ', 1) for header in headers_lines[1:])

    def handle_request(self):
        if self.path == '/':
            status = '200 OK'
        else:
            status = '404 NOT FOUND'

        server_headers = HTTPHeaders([
            ('Date', time.ctime()),
            ('Server', 'AsynChat 0.1')
        ])
        self.headers_set = [status, server_headers]
        self.log_info('%s:%s %s for %s' % (self.addr[0], self.addr[1], self.request_method, self.path))

        if self.cgi_data and self.request_method == 'POST':
            self.handle_post()
        else:
            self.handle_get()
        self.close()

    def handle_post(self):
        response_body = """
<html>
<head>
<title>WOW</title>
</head>
<body>
<h2>Hello {name}</h2>

<p>Your mail is {mail}</p>
</body>
</html>
        """.format(**self.cgi_data)
        status, response_headers = self.headers_set
        response_headers.update(dict([('Content-Type', 'text/html'),
                                      ('Content-Length', len(response_body))]))
        response = 'HTTP/1.1 {status}\r\n'.format(status=status)
        for header in response_headers.items():
            response += "{0}: {1}\r\n".format(*header)
        response += '\r\n'
        response += response_body

        self.push(response.encode('utf-8'))

    def handle_get(self):
        if self.path == '/':
            response_body = """
<html>
<head>
<title>WOW</title>
</head>
<body>
<h2>Wow, Python Server</h2>

<p>Hello World</p>

<form method="post" action="">
Input Your name: <input type="text" name="name"><br>
Input Your mail: <input type='mail' name='mail'><br>
<input type="submit" value="Submit">

</form>
</body>
</html>
        """
        else:
            response_body = """
<html>
<head>
<title>WOW</title>
</head>
<body>
<h2>Oops ...  The page is not found</h2>

</body>
</html>
            """

        status, response_headers = self.headers_set
        response_headers.update(dict([('Content-Type', 'text/html'),
                                      ('Content-Length', len(response_body))]))
        response = 'HTTP/1.1 {status}\r\n'.format(status=status)
        for header in response_headers.items():
            response += "{0}: {1}\r\n".format(*header)
        response += '\r\n'
        response += response_body

        self.push(response.encode('utf-8'))

    def parse(self, headers, data):
        return dict([expr.split('=') for expr in data.split('&')])

    def collect_incoming_data(self, data):
        """Buffer the data"""
        self.ibuffer.append(data)

    def found_terminator(self):
        if self.reading_headers:
            self.reading_headers = False
            self.parse_headers(b''.join(self.ibuffer).decode('utf-8'))
            self.ibuffer = []
            if self.request_method.upper() == "POST":
                clen = self.headers.getheader("Content-Length")
                self.set_terminator(int(clen))
            else:
                self.handling = True
                self.set_terminator(None)
                self.handle_request()
        elif not self.handling:
            self.set_terminator(None)  # browsers sometimes over-send
            self.cgi_data = self.parse(self.headers, b''.join(self.ibuffer).decode('utf-8'))
            self.handling = True
            self.ibuffer = []
            self.handle_request()


class HTTPServer(dispatcher):
    def __init__(self, port):
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(5)

    def handle_accept(self):
        conn, addr = self.accept()
        HTTPHandler(conn, addr)


if __name__ == '__main__':
    h = HTTPServer(PORT)
    asyncore.loop()

```

还可以使用 asynchat 实现聊天室功能。

```
# -*- coding: utf-8 -*-

import sys
import socket
import asyncore
from asyncore import dispatcher
from asynchat import async_chat

PORT = 5005
NAME = 'TestChat'

if sys.version_info.major == 3:
    unicode = str


class EndSession(Exception):
    pass


class CommandHandler(object):

    def unknown(self, session, cmd):
        session.push('Unknown command: %s\n' % cmd)

    def handle(self, session, line):
        if not line.strip():
            return
        parts = line.split(' ', 1)
        cmd = parts[0]
        try:
            line = parts[1].strip()
        except IndexError:
            line = ''
        method = getattr(self, 'do_'+cmd, None)
        try:
            method(session, line)
        except TypeError:
            self.unknown(session, cmd)


class Room(CommandHandler):

    def __init__(self, server):
        self.server = server
        self.sessions = []

    def add(self, session):
        self.sessions.append(session)

    def remove(self, session):
        self.sessions.remove(session)

    def broadcast(self, line):
        for session in self.sessions:
            session.push(line)

    def do_logout(self, session, line):
        raise EndSession


class LoginRoom(Room):

    def add(self, session):
        Room.add(self, session)
        self.broadcast('Welcome to %s\n' % self.server.name)

    def unknown(self, session, cmd):
        session.push('Please log in\nUse "login <nickname>"\n')

    def do_login(self, session, line):
        name = line.strip()
        if not name:
            session.push('Please enter a name\n')
        elif name in self.server.users:
            session.push('The name "%s" is taken.\n' % name)
            session.push('Please try again.\n')
        else:
            session.name = name
            session.enter(self.server.main_room)


class ChatRoom(Room):

    def add(self, session):
        self.broadcast(session.name + ' has entered the room.\n')
        self.server.users[session.name] = session
        Room.add(self, session)

    def remove(self, session):
        Room.remove(self, session)
        self.broadcast(session.name + ' has left the room\n')

    def do_say(self, session, line):
        self.broadcast(session.name + ' : ' + line + '\n')

    def do_look(self, session, line):
        session.push('The following are in the room:\n')
        for other in self.sessions:
            session.push(other.name + '\n')

    def do_who(self, session, line):
        session.push('The following are logged in:\n')
        for name in self.server.users:
            session.push(name + '\n')


class LogoutRoom(Room):

    def add(self, session):
        try:
            del self.server.users[session.name]
        except KeyError:
            pass


class ChatSession(async_chat):

    def __init__(self, server, sock):
        async_chat.__init__(self, sock)
        self.server = server
        self.set_terminator(b'\n')
        self.data = []
        self.name = None
        self.enter(LoginRoom(server))

    def push(self, data):
        print('>> ' + repr(data))
        if isinstance(data, (str, unicode)):
            data = data.encode('utf-8')
        async_chat.push(self, data)

    def enter(self, room):
        try:
            cur = self.room
        except AttributeError:
            pass
        else:
            cur.remove(self)
        self.room = room
        room.add(self)

    def collect_incoming_data(self, data):
        self.data.append(data)

    def found_terminator(self):
        try:
            line = b''.join(self.data).decode('utf-8')
        except UnicodeDecodeError:
            line = b''.join(self.data).decode('gbk')
        self.data = []
        try:
            print('<< ' + repr(line))
            self.room.handle(self, line)
        except EndSession:
            self.handle_close()

    def handle_close(self):
        async_chat.handle_close(self)
        self.enter(LogoutRoom(self.server))


class ChatServer(dispatcher):

    def __init__(self, port, name):
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(5)
        self.name = name
        self.users = {}
        self.main_room = ChatRoom(self)

    def handle_accept(self):
        conn, addr = self.accept()
        ChatSession(self, conn)

if __name__ == '__main__':
    s = ChatServer(PORT, NAME)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print()

```

本想同样使用 asyncore 实现客户端的异步，但是在 Windows 不支持对文件对象的异步，只能对 socket 异步。

所以在 Windows 实现的客户端不能实现自动更新，在 Linux 下的客户端可以自动刷新显示数据。

Windows 

```
# -*- coding: utf-8 -*-

import time
import socket
import asynchat
import asyncore
from asyncore import dispatcher

PORT = 8008


class HTTPHeaders(dict):
    def getheader(self, key):
        return self.get(key)


class HTTPHandler(asynchat.async_chat):
    def __init__(self, sock, addr):
        asynchat.async_chat.__init__(self, sock=sock)
        self.addr = addr
        self.ibuffer = []
        self.obuffer = ""
        self.set_terminator(b'\r\n\r\n')
        self.reading_headers = True
        self.handling = False
        self.cgi_data = None

    def parse_headers(self, data):
        headers_lines = data.split('\r\n')
        self.method, self.path, self.version = headers_lines[0].split()
        self.headers = HTTPHeaders(header.split(': ', 1) for header in headers_lines[1:])

    def handle_request(self):
        if self.path == '/':
            status = '200 OK'
        else:
            status = '404 NOT FOUND'

        server_headers = HTTPHeaders([
            ('Date', time.ctime()),
            ('Server', 'AsynChat 0.1')
        ])
        self.headers_set = [status, server_headers]
        self.log_info('%s:%s %s for %s' % (self.addr[0], self.addr[1], self.method, self.path))

        if self.cgi_data and self.method == 'POST':
            self.handle_post()
        else:
            self.handle_get()
        self.close()

    def handle_post(self):
        response_body = """
<html>
<head>
<title>WOW</title>
</head>
<body>
<h2>Hello {name}</h2>

<p>Your mail is {mail}</p>
</body>
</html>
        """.format(**self.cgi_data)
        status, response_headers = self.headers_set
        response_headers.update(dict([('Content-Type', 'text/html'),
                                      ('Content-Length', len(response_body))]))
        response = 'HTTP/1.1 {status}\r\n'.format(status=status)
        for header in response_headers.items():
            response += "{0}: {1}\r\n".format(*header)
        response += '\r\n'
        response += response_body

        self.push(response.encode('utf-8'))

    def handle_get(self):
        if self.path == '/':
            response_body = """
<html>
<head>
<title>WOW</title>
</head>
<body>
<h2>Wow, Python Server</h2>

<p>Hello World</p>

<form method="post" action="">
Input Your name: <input type="text" name="name"><br>
Input Your mail: <input type='mail' name='mail'><br>
<input type="submit" value="Submit">

</form>
</body>
</html>
        """
        else:
            response_body = """
<html>
<head>
<title>WOW</title>
</head>
<body>
<h2>Oops ...  The page is not found</h2>

</body>
</html>            
            """

        status, response_headers = self.headers_set
        response_headers.update(dict([('Content-Type', 'text/html'),
                                      ('Content-Length', len(response_body))]))
        response = 'HTTP/1.1 {status}\r\n'.format(status=status)
        for header in response_headers.items():
            response += "{0}: {1}\r\n".format(*header)
        response += '\r\n'
        response += response_body

        self.push(response.encode('utf-8'))

    def parse(self, headers, data):
        return dict([expr.split('=') for expr in data.split('&')])

    def collect_incoming_data(self, data):
        """Buffer the data"""
        self.ibuffer.append(data)

    def found_terminator(self):
        if self.reading_headers:
            self.reading_headers = False
            self.parse_headers(b''.join(self.ibuffer).decode('utf-8'))
            self.ibuffer = []
            if self.method.upper() == "POST":
                clen = self.headers.getheader("Content-Length")
                self.set_terminator(int(clen))
            else:
                self.handling = True
                self.set_terminator(None)
                self.handle_request()
        elif not self.handling:
            self.set_terminator(None)  # browsers sometimes over-send
            self.cgi_data = self.parse(self.headers, b''.join(self.ibuffer).decode('utf-8'))
            self.handling = True
            self.ibuffer = []
            self.handle_request()


class HTTPServer(dispatcher):
    def __init__(self, port):
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(5)

    def handle_accept(self):
        conn, addr = self.accept()
        print('%s:%s connected' % addr)
        HTTPHandler(conn, addr)


if __name__ == '__main__':
    h = HTTPServer(PORT)
    asyncore.loop()

```

Linux 的客户端

```
# -*- coding: utf-8 -*-

import sys
import socket
import select


class ChatHandler(object):

    def __init__(self, url, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((url, port))

    def handle(self, cmd, line):
        method = getattr(self, cmd, None)
        if method is None:
            method = self.unknown
        try:
            method(line.encode('utf-8'))
        except UnicodeDecodeError:
            try:
                method(line.decode('utf-8').encode('utf-8'))
            except UnicodeDecodeError:
                method(line.decode('gbk').encode('utf-8'))

    def unknown(self, data):
        self.sock.send(data)


class ChatClient(ChatHandler):

    def __init__(self, url, port):
        super(ChatClient, self).__init__(url, port)
        self.select()

    def login(self, data):
        self.sock.send(data)

    def say(self, data):
        self.sock.send(data)

    def logout(self, data):
        self.sock.close()
        sys.exit(0)

    def select(self):
        while True:
            r, w, e = select.select([sys.stdin, self.sock], [], [])
            for sock in r:
                if sock == self.sock:
                    self.handle_read()
                else:
                    self.handle_write()

    def handle_read(self):
        data = self.sock.recv(1024).decode('utf-8')
        if not data:
            sys.stdout.write('Disconnected from server\n')
            sys.exit(0)
        sys.stdout.write(data)
        sys.stdout.flush()

    def handle_write(self):
        data = sys.stdin.readline()
        sys.stdout.flush()
        try:
            cmd = data.split(' ', 1)[0]
        except ValueError:
            sys.stdout.write('Your input is wrong')
            sys.stdout.flush()
            return
        self.handle(cmd, data)

if __name__ == '__main__':
    c = ChatClient('127.0.0.1', 5005)

```
