# coding=utf-8

import time
import socket
import urllib
import urlparse

desc_host = '127.0.0.1'
desc_port = 8080

source_url = "http://127.0.0.1:5002/"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((desc_host, desc_port))

print "Proxying to %s:%s ..."%(desc_host, desc_port)

while 1:
    server.listen(5)
    conn, addr = server.accept()
    request = conn.recv(1024).split(" ")[1]
    page = urllib.urlopen(urlparse.urljoin(source_url + request)).read()
    print time.strftime('%Y-%m-%d %H:%M:%S')," [%s:%s] %s"%(addr[0], addr[1], request)
    conn.sendall(page)
    conn.close()