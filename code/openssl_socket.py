# coding=utf-8

import socket, sys

def sendall(s, buf):
	byteswritten = 0
	while byteswritten < len(buf):
		byteswritten += s.write(buf[byteswritten:])

print "Creating socket ... "
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "Done. "

print "Connecting to remote host ... "
s.connect(('www.baidu.com',443))
print "Done. "

print "Establishing SSL ... "
ssl = socket.ssl(s)
print "Done. "

print "Requesting document ... "
sendall(ssl, 'GET / HTTP/1.1\r\n\r\n')
print "Done. "

s.shutdown(1)

while 1:
	try:
		buf = ssl.read(1024)
	except socket.sslerror, err:
		if (err[0]) in [socket.SSL_ERROR_ZERO_RETURN, socket.SSL_ERROR_EOF]:
			break
		elif (err[0]) in [socket.SSL_ERROR_WANT_READ, socket.SSL_ERROR_WANT_WRITE]:
			continue
		raise
	if len(buf) == 0:
		break
	sys.stdout.write(buf)

s.close()
