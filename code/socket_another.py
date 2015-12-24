#coding=utf-8
import socket,select,sys

host = sys.argv[1]
port = int(sys.argv[2])
name = sys.argv[3]

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.connect((host,port))
s.sendall("NAME:"+name)
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



