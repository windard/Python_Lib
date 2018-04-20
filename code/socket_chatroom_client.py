# -*- coding: utf-8 -*-

import sys
import socket
import gevent
from gevent import monkey

monkey.patch_all()


host = "127.0.0.1"
port = 8081


def read(s):
    while 1:
        buf = s.recv(1024)
        sys.stdout.write("Received From Sercer : " + buf)
        sys.stdout.flush()


def write(s):
    while 1:
        sys.stdin.flush()
        message = sys.stdin.readline()
        s.send(message)


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    spawns = []
    spawns.append(gevent.spawn(read, s))
    spawns.append(gevent.spawn(write, s))
    gevent.joinall(spawns)


if __name__ == '__main__':
    main()
