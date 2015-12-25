#coding=utf-8
import socket,sys

host = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
	s.connect((host,port))
	print "Connect Successful" 
except:
	print "Connect Failed"

s.send("hello server")

buf = s.recv(1024)
print "Received From Server : " + buf
