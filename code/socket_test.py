'''
Created on 2012-1-6
The echo server example from the socket section can be extanded to watche for more than
one connection at a time by using select() .The new version starts out by creating a nonblocking
TCP/IP socket and configuring it to listen on an address
@author: xiaojay
'''
import select
import socket
import Queue
 
#create a socket
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setblocking(False)
#set option reused
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR  , 1)
 
server_address= ('127.0.0.1',10001)
server.bind(server_address)
 
server.listen(10)
 
#sockets from which we except to read
inputs = [server]
 
#sockets from which we expect to write
outputs = []
 
#Outgoing message queues (socket:Queue)
message_queues = {}
 
#A optional parameter for select is TIMEOUT
timeout = 20
 
while inputs:
    print "waiting for next event"
    readable , writable , exceptional = select.select(inputs, outputs, inputs, timeout)
 
    # When timeout reached , select return three empty lists
    if not (readable or writable or exceptional) :
        print "Time out ! "
        break;    
    for s in readable :
        if s is server:
            # A "readable" socket is ready to accept a connection
            connection, client_address = s.accept()
            print "    connection from ", client_address
            connection.setblocking(0)
            inputs.append(connection)
            message_queues[connection] = Queue.Queue()
        else:
            data = s.recv(1024)
            if data :
                print " received " , data , "from ",s.getpeername()
                message_queues[s].put(data)
                # Add output channel for response    
                if s not in outputs:
                    outputs.append(s)
            else:
                #Interpret empty result as closed connection
                print "  closing", client_address
                if s in outputs :
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                #remove message queue 
                del message_queues[s]
    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except Queue.Empty:
            print " " , s.getpeername() , 'queue empty'
            outputs.remove(s)
        else:
            print " sending " , next_msg , " to ", s.getpeername()
            s.send(next_msg)
     
    for s in exceptional:
        print " exception condition on ", s.getpeername()
        #stop listening for input on the connection
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        #Remove message queue
        del message_queues[s]