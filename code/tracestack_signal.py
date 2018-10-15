# -*- coding: utf-8 -*-
import traceback
import signal
import socket
import time


host = "127.0.0.1"
port = 8081

# s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# s.bind((host,port))
# s.listen(5)

print "Server is running on port %s Press Ctrl-C to stop"%port
signal.signal(signal.SIGUSR2, lambda num,stack:traceback.print_stack(stack))


while 1:
    time.sleep(10)
    print '10 seconds sheep'
    # clientsock, clientaddr = s.accept()
    # print "Welcome from %s:%s"%(clientaddr[0],clientaddr[1])
    # while 1:
    #     request = clientsock.recv(1024)
    #     print "Received From client : %r" % request
    #     if not request:
    #         break
    #     clientsock.send("Hello client:%s" % request)
