#coding=utf-8
import socket,select
import sys

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(('127.0.0.1',8090))
s.listen(10)

print "Server is running ... "

inputs = [0,s]
outputs = []
clients = {}

while True:
	try:
		readable,writeable,exceptional = select.select(inputs,outputs,[])
		for sock in readable:
			if sock == s:
				clientsock,clientaddr = sock.accept()
				clientname =clientsock.recv(1024).split('NAME:')[1]
				clientsock.sendall("Welcome " + clientname + "\n")
				print clientname + " Come In"
				clients[clientsock] = (clientname,clientaddr,clientsock)
				inputs.append(clientsock)
				for output in outputs:
					output.sendall("Welcome " + clientname + " Come In \n")
				outputs.append(clientsock)
			elif sock == 0:
				message = sys.stdin.readline()
				if message.startswith("QUIT"):
					print "Server is close ... "
					sys.exit(0)
				for output in outputs:
					output.sendall("Server : " + message)			
			else:
				data = sock.recv(1024)
				if data:
					if data.startswith("SECRECT"):
						print "SECRECT " + clients[sock][0] + " : " + data,
						output = data.split(" ")[1]
						message = data.split(" ")[2]
						for client in clients.values():
							if client[0] == output:
								client[2].sendall("SECRECT " + clients[sock][0] + " : " + message)
					else:
						print clients[sock][0] + " : " + data,
						for output in outputs:
							if output != sock:
								output.sendall(clients[sock][0] + " : " + data)
				else:
					name = clients[sock][0]
					print name+" leaved "
					for output in outputs:
						output.sendall(name+" leaved \n")
					inputs.remove(sock)
					outputs.remove(sock)
					del clients[sock]


	except KeyboardInterrupt:
		print "Server is close ... "
		break




