# coding=utf-8

import socket
from time import ctime

host = '127.0.0.1'
port = 1234
bufsize = 1024

udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpsock.bind((host, port))

while 1:
	print "Waiting for message ... "
	data , addr = udpsock.recvfrom(bufsize)
	udpsock.sendto('[%s] %s'%(ctime(), data), addr)
	print ' ... received from and teturned to:', addr

udpsock.close()