#coding=utf-8

import sys
import socket
import select
import threading
import argparse

def readFromStdin(s):
	while 1:
		data = sys.stdin.readline()
		if data.lower().startswith("quit"):
			s.stopFlag = True
			break
		else:
			for client in s.outputs:
				client.sendall("Server : "+data)

class ChatroomServer(object):
	"""docstring for ChatroomServer"""
	def __init__(self, host , port):
		self.host = host
		self.port = port
		self.stopFlag = False
		self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		self.inputs = [self.s]
		self.outputs = []
		self.clients = {}

	def run(self):
		self.s.bind((self.host,self.port))
		self.s.listen(100)
		print unicode("Server is running ... ","utf-8")

		threading.Thread(target=readFromStdin,args=(self,)).start()

		while 1:
			try:
				if self.stopFlag:
					print unicode("Server is close ...","utf-8")
					break
				readable,writeable,exceptional = select.select(self.inputs,self.outputs,[])
				for sock in readable:
					if sock == self.s:
						clientsock,clientaddr = sock.accept()
						recvname = clientsock.recv(1024)
						if recvname.startswith("NAME:"):
							clientname = recvname.split('NAME:')[1]
						else:
							clientname = str(clientaddr)
						clientsock.sendall("Welcome " + clientname + "\n")
						# print unicode(clientname + " Come In","utf-8")
						print clientname
						self.clients[clientsock] = (clientname,clientaddr,clientsock)
						self.inputs.append(clientsock)
						for output in self.outputs:
							output.sendall("Welcome " + clientname + " Come In \n")
						self.outputs.append(clientsock)
					elif sock == 0:
						message = sys.stdin.readline()
						if message.startswith("QUIT"):
							print unicode("Server is close ... ","utf-8")
							sys.exit(0)
						for output in self.outputs:
							output.sendall("Server : " + message)			
					else:
						try:
							data = sock.recv(1024)
						except Exception,e:
							print unicode("falied %s"%e.message,"utf-8")
							name = self.clients[sock][0]
							# print unicode(name+" leaved ","utf-8")
							print name+" leaved "
							self.inputs.remove(sock)
							self.outputs.remove(sock)
							for output in self.outputs:
								output.sendall(name+" leaved \n")
							del self.clients[sock]
						if data:
							if data.startswith("SECRECT"):
								print unicode("SECRECT " + self.clients[sock][0] + " : " + data,"utf-8")
								output = data.split(" ")[1]
								message = data.split(" ")[2]
								for client in self.clients.values():
									if client[0] == output:
										client[2].sendall("SECRECT " + self.clients[sock][0] + " : " + message)
							else:
								# print unicode(self.clients[sock][0] + " : " + data,"utf-8")
								print self.clients[sock][0] + " : " + data
								for output in self.outputs:
									if output != sock:
										output.sendall(self.clients[sock][0] + " : " + data)
						else:
							name = self.clients[sock][0]
							# print unicode(name+" leaved ","utf-8")
							print name+" leaved "
							self.inputs.remove(sock)
							self.outputs.remove(sock)
							for output in self.outputs:
								output.sendall(name+" leaved \n")
							del self.clients[sock]

			except KeyboardInterrupt:
				print unicode("Server is close ... ","utf-8")
				break

	def close(self):
		self.s.close()

class ChatroomClient(object):
	"""docstring for ChatroomClient"""
	def __init__(self,host,port,name=None):
		self.host = host
		self.port = port
		self.name = name
		self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

	def run(self):
		self.s.connect((host,port))
		if self.name!=None:
			self.s.sendall("NAME:"+self.name)
		else:
			self.s.sendall("Anonymous")

		# print unicode(self.s.recv(1024),"utf-8")
		print self.s.recv(1024)

		threading.Thread(target=clientInput,args=(self,)).start()

		while 1:
			try:
				readable,writeable,exceptional = select.select([self.s],[],[])
				for sock in readable:
					if sock == self.s:
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
						self.s.sendall(data)
			except KeyboardInterrupt:
				print unicode("Client is closed","utf-8")
				break
			except Exception,e:
				print unicode("failed"+e.message,"utf-8")

def clientInput(s):
	while 1:
		data = sys.stdin.readline()
		s.s.sendall(data)
		if data.lower().startswith("quit"):
			s.s.shutdown(socket.SHUT_RDWR)
			s.s.close()
			break

if __name__ == '__main__':
	typename = raw_input("Please chose the type :server|client >>> ")
	if typename.lower().startswith("server"):
		host = raw_input("Please input your host : IP Adress >>> ")
		port = int(raw_input("input your port :1024-65535 >>> "))
		server = ChatroomServer(host,port)
		server.run()
	elif typename.lower().startswith("client"):
		host = raw_input("Please input your host : IP Adress >>> ")
		port = int(raw_input("Please input your port :1024-65535 >>> "))
		name = raw_input("Please input your name >>> ")
		client = ChatroomClient(host,port,name)
		client.run()