# coding=utf-8

import sys
import socket
import threading

if len(sys.argv) < 3:
    print("Usage: python server.py 127.0.0.1 8001")
    exit(0)
host = sys.argv[1]
port = int(sys.argv[2])


def server_single():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print("Server is running on port %s Press Ctrl-C to stop" % port)

    try:
        while True:
            client_sock, client_addr = s.accept()
            print("Welcome from %s : %s" % (client_addr[0], client_addr[1]))
            request_data = client_sock.recv(1024)
            print("Received From client: " + request_data)
            client_sock.send("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\n\r\nHello world")
            client_sock.close()
    except KeyboardInterrupt:
        s.close()


def handler(client_sock):
    # type: (socket.socket) -> None
    try:
        # 在使用 while 循环时，浏览器无法正确的识别并关闭连接
        # 不要这样写 HTTP server
        while True:
            request_data = client_sock.recv(1024)
            print("Received From client: " + request_data)
            if not request_data:
                return
            client_sock.sendall("HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\n\r\nHello world\r\n\r\n")
    except Exception as e:
        print("connection error: %r" % e)
        client_sock.close()


def server_thread():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print("Server is running on port %s Press Ctrl-C to stop" % port)

    try:
        while True:
            sock, client_addr = s.accept()
            print("Welcome from %s : %s" % (client_addr[0], client_addr[1]))
            t = threading.Thread(target=handler, args=(sock, ))
            t.setDaemon(True)
            t.start()
    except KeyboardInterrupt:
        s.close()


if __name__ == '__main__':
    server_thread()
