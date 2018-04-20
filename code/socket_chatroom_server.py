# -*- coding: utf-8 -*-

import socket
import thread

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
        clientsock, clientaddr = s.accept()
        socks.append(clientsock)
        thread.start_new_thread(connect, (clientsock, clientaddr, socks))


def connect(clientsock, clientaddr, socks):
    print "Welcome from %s : %s" % (clientaddr[0], clientaddr[1])
    clientsock.sendall("Hello client\n")
    while 1:
        message = clientsock.recv(1024)
        if not len(message):
            socks.remove(clientsock)
            break
        print "Received From %s:%s client : '%s'" % (
            clientaddr[0], clientaddr[1], message.strip())
        for sock in socks:
            if sock == clientsock:
                break
            clientsock.send(message)


if __name__ == '__main__':
    main()
