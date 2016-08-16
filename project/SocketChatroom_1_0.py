#coding=utf-8

import sys
import socket
import select
import argparse

def runserver(host,port):
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	s.bind((host,port))
	s.listen(10)

	print unicode("Server is running ... ","utf-8")

	inputs = [s]
	outputs = []
	clients = {}

	while True:
		try:
			readable,writeable,exceptional = select.select(inputs,outputs,[])
			for sock in readable:
				if sock == s:
					clientsock,clientaddr = sock.accept()
					recvname = clientsock.recv(1024)
					if recvname.startswith("NAME:"):
						clientname = recvname.split('NAME:')[1]
					else:
						clientname = str(clientaddr)
					clientsock.sendall("Welcome " + clientname + "\n")
					print unicode(clientname + " Come In","utf-8")
					clients[clientsock] = (clientname,clientaddr,clientsock)
					inputs.append(clientsock)
					for output in outputs:
						output.sendall("Welcome " + clientname + " Come In \n")
					outputs.append(clientsock)
				elif sock == 0:
					message = sys.stdin.readline()
					if message.startswith("QUIT"):
						print unicode("Server is close ... ","utf-8")
						sys.exit(0)
					for output in outputs:
						output.sendall("Server : " + message)			
				else:
					data = sock.recv(1024)
					if data:
						if data.startswith("SECRECT"):
							print unicode("SECRECT " + clients[sock][0] + " : " + data,"utf-8")
							output = data.split(" ")[1]
							message = data.split(" ")[2]
							for client in clients.values():
								if client[0] == output:
									client[2].sendall("SECRECT " + clients[sock][0] + " : " + message)
						else:
							print unicode(clients[sock][0] + " : " + data,"utf-8")
							for output in outputs:
								if output != sock:
									output.sendall(clients[sock][0] + " : " + data)
					else:
						name = clients[sock][0]
						print unicode(name+" leaved ","utf-8")
						for output in outputs:
							output.sendall(name+" leaved \n")
						inputs.remove(sock)
						outputs.remove(sock)
						del clients[sock]

		except KeyboardInterrupt:
			print unicode("Server is close ... ","utf-8")
			break

def runclient(host,port,name=None):
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	s.connect((host,port))
	if name!=None:
		s.sendall("NAME:"+name)
	else:
		s.sendall("NAME:")

	print unicode(s.recv(1024),"utf-8")

	while True:
		try:
			readable,writeable,exceptional = select.select([s],[],[])
			for sock in readable:
				if sock == s:
					data = sock.recv(1024)
					if not data:
						print unicode("Server is closed","utf-8")
						sys.exit(0)
					sys.stdout.write(data)
					sys.stdout.flush()
				else:
					data = sys.stdin.readline()
					if data.startswith("QUIT"):
						print unicode("Client is closed","utf-8")
						sys.exit(0)
					s.sendall(data)
		except KeyboardInterrupt:
			print unicode("Client is closed","utf-8")
			break

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="socket chatroom")
	parser.add_argument("--type",help="chose the type :server|client",action="store",default="client",dest="type")
	parser.add_argument("--host",help="input your host : IP Adress",action="store",default="127.0.0.1",dest="host")
	parser.add_argument("--port",help="input your port :1024-65535",action="store",default=8888,type=int,dest="port")
	parser.add_argument("--name",help="input your name ",action="store",default=None,dest="name")
	args = parser.parse_args()
	chattype = args.type
	host = args.host
	port = args.port
	name = args.name
	if chattype.startswith("server"):
		runserver(host,port)
	elif chattype.startswith("client"):
		runclient(host,port,name)
	else:
		print unicode("your input is wrong","utf-8")

