# -*- coding: utf-8 -*-

import socket
import threading

host = "127.0.0.1"
port = 8081


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    socks = []

    print "Server is running on %s:%s Press Ctrl-C to stop" % (host, port)

    while 1:
        clientsock, _ = s.accept()
        socks.append(clientsock)
        threading.Thread(target=connect, args=(clientsock, socks)).start()


def connect(clientsock, socks):
    clientaddr = '%s:%5s' % (clientsock.getpeername())
    print "Welcome from %s" % (clientaddr)
    clientsock.sendall("Hello client")
    while 1:
        message = clientsock.recv(1024)
        if not len(message):
            socks.remove(clientsock)
            break
        data = '%s : %s' % (clientaddr, message.strip())
        print(data)
        for sock in socks:
            if sock == clientsock:
                continue
            sock.sendall(data)


if __name__ == '__main__':
    main()
