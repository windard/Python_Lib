#coding=utf-8
import socket,sys

host = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
	s.connect((host,port))
	print "Connect Successful"
	#s.sendall("Hello world")
	response = s.recv()
	print response
except:
	print "Your Connect Is Wrong"
