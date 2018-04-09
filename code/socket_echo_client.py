# -*- coding: utf-8 -*-

import sys
import socket


host = "127.0.0.1"
port = 8081


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    while 1:
        buf = s.recv(1024)
        sys.stdout.write("Received From Sercer : " + buf)
        sys.stdout.flush()
        sys.stdin.flush()
        message = sys.stdin.readline()
        s.send(message)


if __name__ == '__main__':
    main()
