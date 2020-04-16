# coding=utf-8

import sys
import socket

host = sys.argv[1]
port = int(sys.argv[2])


def client_demo():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        print("Connect Successful")
    except Exception as e:
        print("Connect Failed, error: %r" % e)
        exit(0)

    s.send("hello server")

    buf = s.recv(1024)
    print("Received From Server : " + buf)


def client_cli():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        print("Connect Successful")
    except Exception as e:
        print("Connect Failed, error: %r" % e)
        exit(0)

    data = "GET / HTTP/1.1\r\n\r\n"
    print("send: " + repr(data))
    s.sendall(data)
    buf = s.recv(1024)
    print("Received From Server : " + buf)

    while True:
        # 因为在 Python 下无法输入 `\r` 比较困难😪
        # 所以不要用 这个客户端了，用 nc 吧
        data = raw_input("Input: ")
        if not data.decode("utf-8"):
            break
        print("send: " + repr(data))
        s.sendall(data)
        buf = s.recv(1024)
        print("Received From Server : " + buf)


def client_http():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        print("Connect Successful")
    except Exception as e:
        print("Connect Failed, error: %r" % e)
        exit(0)

    s.send("GET /ping HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n")

    buf = s.recv(1024)
    print("Received From Server : " + repr(buf))


if __name__ == '__main__':
    client_http()
