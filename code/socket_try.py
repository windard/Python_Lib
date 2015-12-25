#coding=utf-8
import socket,select

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(('127.0.0.1',8090))
s.listen(5)

print "Now are waiting"

inputs = [s]
outputs = []
clients = {}

while 1:
	# clientsock,clientaddr = s.accept()
	# print "%s connect"%clientaddr
	readable,writeable,exceptional = select.select(inputs,outputs,[])
	for sock in readable:
		# print sock
		if sock == s:
			clientsock,clientaddr = sock.accept()
			clientsock.send("Welcome")
			clients[clientsock] = (clientsock,clientaddr)
			inputs.append(sock)
			# print "%s come in"%clientaddr
			outputs.append(sock)
			print "someone comein"
			# for output in outputs:
			# 	output.sendall("New Comer")			
		else:
			print "NI chulai"
			# print sock
			data = s.recv(1024)
			print data



