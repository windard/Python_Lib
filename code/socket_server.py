#coding=utf-8

import socket

host = "127.0.0.1"
port = 8081

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))
s.listen(5)

print "Server is running on port %s Press Ctrl-C to stop"%port

while 1:
	clientsock,clientaddr = s.accept()
	print "Welcome from %s : %s"%(clientaddr[0],clientaddr[1])
	resquest = clientsock.recv(1024)
	print "Received From client : " + resquest
	clientsock.send("Hello client")
	clientsock.close()

s.close()
