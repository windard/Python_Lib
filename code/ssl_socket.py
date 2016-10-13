# coding=utf-8

import socket,sys

def sendall(s,buf):
    bytewritten = 0
    while bytewritten < len(buf):
        bytewritten += s.write(buf[bytewritten:])

print "Create Socket ... "

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print "DONE"

print "Connecting to remote host ... "
s.connect(('www.baidu.com',443))
print "DONE"

print "Establishing SSL ... "
ssl = socket.ssl(s)
print   "DONE"

print "Requesting doument ... "
sendall(ssl,'GET / HTTP/1.0\r\n\r\n')
print   "DONE"

s.shutdown(1)

while 1:
    try:
        buf = ssl.read(1024)
    except socket.sslerror,err:
        if err[0] in [socket.SSL_ERROR_ZERO_RETURN,socket.SSL_ERROR_EOF]:
            break
        elif err[0] in [socket.SSL_ERROR_WANT_READ,socket.SSL_ERROR_WANT_WRITE]:
            continue
        raise
    if len(buf) == 0:
        break
    sys.stdout.write(buf)

s.close()
