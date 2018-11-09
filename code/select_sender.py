# -*- coding: utf-8 -*-
import sys
import time
import random
import socket

host = '127.0.0.1'
port = 8760


def handle_serve(host, port):

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host,port))
    server.listen(5)

    print "Server is running on %s:%s Press Ctrl-C to stop" % (host, port)

    while 1:
        clientsock,clientaddr = server.accept()
        print "Welcome from %s : %s"%(clientaddr[0],clientaddr[1])
        while 1:
            time.sleep(random.randint(2, 7))
            clientsock.sendall(str(time.time())+"\n")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    handle_serve(host, port)
