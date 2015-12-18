#coding=utf-8

import threading
import argparse
from Queue import Queue
import socket  
import sys

def scan(host,port,show):  
	s = socket.socket()  
	protocolname = 'tcp'
	s.settimeout(0.1)
	if s.connect_ex((host, port)) == 0:  
		try:
			print "%s  open => service name: %s" %(port,socket.getservbyport(port,protocolname))
		except:
			print port, 'open => service name: No Found'  
	else:
		if show:
			print port ,'Close'
	s.close()  

def writeQ(queue,start,end):
	for i in range(start,end):
		queue.put(i,1)

def readQ(queue,host,start,end,show,thread):
	for i in range((end-start)/thread):
		num = queue.get(1)
		scan(host,num,show)

def thread_demo(host,port_start,port_end,show,thread):
	funcs = [writeQ,readQ]
	nfunc = range(len(funcs))
	q = Queue(65535)
	threads = []
	t = threading.Thread(target=funcs[0],args=(q,port_start,port_end))
	threads.append(t)	
	for i in range(thread):
		t = threading.Thread(target=funcs[1],args=(q,host,port_start,port_end,show,thread))
		threads.append(t)	
	for i in range(thread+1):
		threads[i].start()
	for i in range(thread+1):
		threads[i].join()

if __name__ == '__main__':  
	parser = argparse.ArgumentParser(description="input your host and port")
	parser.add_argument("-o","--on",help="show close",action="store_true")
	parser.add_argument("--host",help="chose host",action="store",default='127.0.0.1',dest="host")
	parser.add_argument("--host_start",help="chose host_start",action="store",default='127.0.0.1',dest="host_start")
	parser.add_argument("--host_end",help="chose host_end",action="store",default='127.0.0.1',dest="host_end")
	parser.add_argument("--port",help="chose port",action="store",default=80,type=int,dest="port")
	parser.add_argument("--port_start",help="chose port port_start",action="store",type=int,default=0,dest="port_start")
	parser.add_argument("--port_end",help="chose port port_end",action="store",type=int,default=512,dest="port_end")
	parser.add_argument("--thread",help="how much thread",action="store",type=int,default=4,dest="thread")
	args = parser.parse_args()
	host = args.host
	host_start = args.host_start
	host_end   = args.host_end
	port = args.port
	port_start = args.port_start
	port_end   = args.port_end
	thread = args.thread
	show = args.on
	if host == "127.0.0.1":
		for hosts in range(int(host_start.split(".")[-1]),int(host_end.split(".")[-1])+1):
			hosts = host_start.split(".")[0]+"."+host_start.split(".")[1]+"."+host_start.split(".")[2]+"."+str(hosts)
			print "----------"+hosts+"----------"
			if host_start != host_end and port_start == 0 and port_end == 512:
				scan(hosts,port,show)
			elif host_start != host_end and port_start != 0 or port_end != 512:
				thread_demo(hosts,port_start,port_end+1,show,thread)
			elif host_start == host_end and port == 80:
				thread_demo(hosts,port_start,port_end+1,show,thread)
			elif host_start == host_end and port != 80:
				scan(hosts,port,show)
			else:
				print "En... Your Input Is Wrong"
	else:
		print "----------"+host+"----------"
		if port != 80:
			scan(host,port,show)
		else:
			thread_demo(host,port_start,port_end+1,show,thread)

				