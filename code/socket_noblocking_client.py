# coding=utf-8

import socket


host = "127.0.0.1"
port = 8082

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((host, port))
    print "Connect Successful"
except Exception as e:
    print "Connect Failed"

s.send("hello server")

buf = s.recv(1024)
print "Received From Server : " + buf
s.send("1")
