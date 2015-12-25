#coding=utf-8

import sys
import socket
import select
import argparse

def runclient(host,port,name):
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	s.connect((host,port))
	if name:
		s.sendall("NAME:"+name)
	else:
		s.sendall("NAME:")
	print s.recv(1024),

	while True:
		try:
			readable,writeable,exceptional = select.select([0,s],[],[])
			for sock in readable:
				if sock == s:
					data = sock.recv(1024)
					if not data:
						print "Server is closed"
						sys.exit(0)
					sys.stdout.write(data)
					sys.stdout.flush()
				else:
					data = sys.stdin.readline()
					if data.startswith("QUIT"):
						print "Client is closed"
						sys.exit(0)
					s.sendall(data)
		except KeyboardInterrupt:
			print "Client is closed"
			break

if __name__ == '__main__':
	# parser = argparse.ArgumentParser(description="socket chatroom")
	# parser.add_argument("--host",help="input your host",action="store",default="127.0.0.1",dest="host")
	# parser.add_argument("--port",help="input your port",action="store",default=8888,type=int,dest="port")
	# parser.add_argument("--name",help="input your name",action="store",default=None,dest="name")
	# args = parser.parse_args()
	# host = args.host
	# port = args.port
	# name = args.name
	host = sys.argv[1]
	port = int(sys.argv[2])
	name = sys.argv[3]
	runclient(host,port,name)

