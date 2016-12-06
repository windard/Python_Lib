# coding=utf-8

import socket

host = '127.0.0.1'
port = 1234

bufsize = 1024

udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while 1:
	data = raw_input(">")
	if not data:
		break
	udpsock.sendto(data, (host, port))
	data, addr = udpsock.recvfrom(bufsize)
	if not data:
		break
	print data

udpsock.close()