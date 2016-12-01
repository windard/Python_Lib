# coding=utf-8

import time
import socket
import urllib

host = '127.0.0.1'
port = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
print "server is running ... "

while 1:
	server.listen(5)
	ss,addr = server.accept()
	url = "http://127.0.0.1:5002/"
	request = ss.recv(1024).split(" ")[1]
	page = urllib.urlopen(url+request).read()
	print time.strftime('%Y-%m-%d %H:%M:%S')," [%s:%s] %s"%(addr[0],addr[1],request)
	ss.sendall(page)
	ss.close()
