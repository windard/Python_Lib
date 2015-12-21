#coding=utf-8
import socket,sys

host = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
	s.connect((host,port))
	print "Connect Successful"
	response = s.recv(2048)
	print response
except:
	print "Your Connect Is Wrong"