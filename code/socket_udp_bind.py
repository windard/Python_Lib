# -*- coding: utf-8 -*-

import sys
import socket
import threading

host = '127.0.0.1'
port = 1234
bufsize = 1024


def server(udpsock):
    print "Waiting for message ... "
    while 1:
        data, addr = udpsock.recvfrom(bufsize)
        print '[%s:%s]: %s' % (addr[0], addr[1], data)


def main(host, port):

    udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpsock.bind((host, port))
    thread = threading.Thread(target=server, args=(udpsock,))
    thread.setDaemon(True)
    thread.start()

    import pdb
    pdb.set_trace()

    while 1:
        data = raw_input(">")
        if not data:
            break
        udpsock.sendto(data, (host, port))

    udpsock.close()


if __name__ == '__main__':
    if len(sys.argv) > 2:
        host = sys.argv[1]
        port = int(sys.argv[2])
    main(host, port)
