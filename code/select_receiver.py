# -*- coding: utf-8 -*-
import select
import socket


host = '127.0.0.1'
soa_port = 8760
sob_port = 8761


def handle_client(soa, sob):
    fdset = [soa, sob]
    while True:
        r, w, e = select.select(fdset, [], [])
        for sock in r:
            data = sock.recv(1024)
            print sock.getsockname(), data,


if __name__ == '__main__':
    soa = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soa.connect((host, soa_port))

    sob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sob.connect((host, sob_port))

    print dir(soa)
    handle_client(soa, sob)
