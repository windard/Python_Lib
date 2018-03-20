# coding=utf-8

import socket, sys
from OpenSSL import SSL

ctx = SSL.Context(SSL.SSLv23_METHOD)
print "Creating socket ..."
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "Done"

ssl = SSL.Connection(ctx, s)

print "Establishing SSL ..."
ssl.connect(('www.openssl.org', 443))
print "Done"

print "Requesting document ..."
# ssl.sendall("GET / HTTP/1.0\r\n\r\n")
ssl.sendall("GET /\r\n") 
print "Done"

while 1:
	try:
		buf = ssl.recv(4096)
	except SSL.ZeroReturnError:
		break
	sys.stdout.write(buf)

ssl.close()