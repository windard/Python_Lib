#coding=utf-8

import socket
import thread 

def connect(clientsock,clientaddr):
	print "Welcome from %s : %s"%(clientaddr[0],clientaddr[1])
	clientsock.send("Hello client \n")
	while 1:
		resquest = clientsock.recv(1024)		
		while not len(resquest):
			break
		print "Received From No.%s client : "%clientaddr[1] + resquest,


host = "127.0.0.1"
port = 8081

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

old_state = s.getsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR)
print "Old State is : " + str(old_state)

s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
new_state = s.getsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR)
print "New State is : " + str(new_state)

s.bind((host,port))
s.listen(5)

print "Server is running on port %s Press Ctrl-C to stop"%port

while 1:
	clientsock,clientaddr = s.accept()
	thread.start_new_thread(connect ,(clientsock,clientaddr))

s.close()

