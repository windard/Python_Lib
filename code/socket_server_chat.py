#coding=utf-8

import socket
import thread 

host = "127.0.0.1"
port = 8081

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))
s.listen(5)

def connect(clientsock,clientaddr):
	print "Welcome from %s : %s"%(clientaddr[0],clientaddr[1])
	clientsock.send("Hello client")
	while 1:
		resquest = clientsock.recv(1024)		
		if resquest.lower().startswith('q'):
			break
		print "Received From No.%s client : "%clientaddr[1] + resquest,
		message = raw_input('\n')
		clientsock.sendall(message)

print "Server is running on port %s Press Ctrl-C to stop"%port

while 1:
	clientsock,clientaddr = s.accept()
	thread.start_new_thread(connect ,(clientsock,clientaddr))

s.close()

