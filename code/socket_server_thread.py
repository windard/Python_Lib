#coding=utf-8

import socket
import thread 

host = "127.0.0.1"
port = 8081

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))
s.listen(5)

def connect(socket):
	while 1:
		print "Received From client : " + resquest
		socket.send("Hello client")
		buf = socket.recv(1024)
		while not buf:
			break
		print buf

print "Server is running on port %s Press Ctrl-C to stop"%port

while 1:
	clientsock,clientaddr = s.accept()
	print "Welcome from %s : %s"%(clientaddr[0],clientaddr[1])
	resquest = clientsock.recv(1024)
	thread.start_new_thread(connect ,(clientsock,))

s.close()

http://www.cnblogs.com/GarfieldTom/archive/2012/12/16/2820143.html
http://www.centoscn.com/python/2013/0817/1322.html
http://blog.csdn.net/rebelqsp/article/details/22109925