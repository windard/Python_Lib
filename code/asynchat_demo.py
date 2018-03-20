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
