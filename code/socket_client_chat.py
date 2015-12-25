#coding=utf-8
import socket,sys

host = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
try:
	s.connect((host,port))
	print "Connect Successful" 
except:
	print "Connect Failed"

print "Now You Can Chat With Server , Input 'Q' to Quit"
while 1:
	buf = s.recv(1024)
	print "Received From Server : " + buf
	message = raw_input()
	s.sendall(message)
	if message.lower().startswith('q'):
		s.close()
		break
