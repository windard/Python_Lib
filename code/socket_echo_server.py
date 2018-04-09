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

    print "Server is running on %s:%s Press Ctrl-C to stop" % (host, port)

    while 1:
        clientsock, clientaddr = s.accept()
        thread.start_new_thread(connect, (clientsock, clientaddr))


def connect(clientsock, clientaddr):
    print "Welcome from %s : %s" % (clientaddr[0], clientaddr[1])
    clientsock.sendall("Hello client\n")
    while 1:
        message = clientsock.recv(1024)
        if not len(message):
            break
        print "Received From %s:%s client : '%s'" % (
            clientaddr[0], clientaddr[1], message.strip())
        clientsock.send(message)


if __name__ == '__main__':
    main()
