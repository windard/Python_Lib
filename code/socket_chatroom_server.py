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
					if clientsock.recv(1024).endswith("NAME:"):
						clientname = str(clientaddr)
					else:
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

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="socket chatroom")
	parser.add_argument("--host",help="input your host",action="store",default="127.0.0.1",dest="host")
	parser.add_argument("--port",help="input your port",action="store",default=8888,type=int,dest="port")
	args = parser.parse_args()
	host = args.host
	port = args.port
	runserver(host,port)



http://blog.csdn.net/jeanwaljean/article/details/5982292
http://blog.csdn.net/historyasamirror/article/details/5778378
http://www.cnblogs.com/Anker/p/3254269.html
http://www.oschina.net/translate/the-future-of-asynchronous-io-in-python?cmp&p=2
http://www.pythontab.com/html/2013/pythonhexinbiancheng_0325/318.html
http://blog.chinaunix.net/uid-429659-id-5095161.html
http://news.tuxi.com.cn/kf/article/jahtt.htm
http://www.haiyun.me/archives/1056.html
http://wiki.jikexueyuan.com/project/python-actual-combat/tutorial-23.html
http://www.linuxidc.com/Linux/2014-02/97152.htm
http://www.cnblogs.com/coser/archive/2011/12/17/2291160.html
http://www.cnblogs.com/coser/archive/2012/01/06/2315216.html
http://www.cnblogs.com/IPrograming/p/Python-socket.html
http://www.centoscn.com/python/2013/0817/1322.html
http://www.cnblogs.com/GarfieldTom/archive/2012/12/16/2820143.html
https://hit-alibaba.github.io/interview/basic/network/Socket-Programming-Basic.html
http://goodcandle.cnblogs.com/archive/2005/12/10/294652.aspx
http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386832511628f1fe2c65534a46aa86b8e654b6d3567c000