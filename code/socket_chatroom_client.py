# -*- coding: utf-8 -*-

import os
import sys
import socket
import threading


host = "127.0.0.1"
port = 8081


def read(s):
    while 1:
        buf = s.recv(1024)
        sys.stdout.write("\033[2K\033[E")
        sys.stdout.write("\033[34m< " + buf + "\033[39m")
        sys.stdout.write("\n> ")
        sys.stdout.flush()


def write(s):
    while 1:
        message = raw_input("> ")
        if message.strip().lower() == "quit" or \
                message.strip().lower() == "exit":
            s.close()
            os._exit(0)
        s.sendall(message)


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    pw = threading.Thread(target=write, args=(s, ))
    pw.setDaemon(True)
    pw.start()
    pr = threading.Thread(target=read, args=(s, ))
    pr.start()
    pw.join()


if __name__ == '__main__':
    main()
