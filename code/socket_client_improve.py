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

timeout = s.gettimeout()
print timeout

s.settimeout(2)

timeout = s.gettimeout()
print timeout

buf = s.recv(1024)
print "Received From Sercer : " + buf
