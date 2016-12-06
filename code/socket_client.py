#coding=utf-8
import socket,sys

host = "127.0.0.1"
port = 8081

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
	s.connect((host,port))
	print "Connect Successful" 
except:
	print "Connect Failed"

s.send("hello server")

buf = s.recv(1024)
print "Received From Server : " + buf
