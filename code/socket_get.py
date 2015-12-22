#coding=utf-8

import socket

hostname = socket.gethostname()
print "host name : " + hostname

hostip = socket.gethostbyname(hostname)
print "host ip : " + hostip

host = socket.gethostbyaddr(hostip)
for item in host:
	print item

httpport = socket.getservbyname("http")
print "http port : " + str(httpport)

ftpport = socket.getservbyname("ftp","tcp")
print "tcp port : " + str(ftpport)

udpnumber = socket.getprotobyname("udp")
print "udp number is : " + str(udpnumber)

tcpnumber = socket.getprotobyname("tcp")
print "tcp number is : " + str(tcpnumber)

servivename = socket.getservbyport(25)
print "25 port is : " + servivename

servivename = socket.getservbyport(43)
print "43 port is : " + servivename

addrinfo = socket.getaddrinfo("www.baidu.com",None)
for item in addrinfo:
	print "www.baidu.com ip is : " + item[4][0]