#coding=utf-8

import threading
from time import ctime,sleep

class MyThread(threading.Thread):
	def __init__(self,func,args,name=""):
		threading.Thread.__init__(self)
		self.name = name
		self.func = func
		self.args = args

	def run(self):
		apply(self.func,self.args)

def loop(nloop,nsec):
	print "loop",nloop," start at: ",ctime()
	sleep(nsec)
	print "loop",nloop,"end    at: ",ctime()
	
print "all start at: ",ctime()

loops = [4,2]
threads = []
nloops = range(len(loops))

for i in nloops:
	t = MyThread(loop,(i,loops[i]),loop.__name__)
	threads.append(t)	

for i in nloops:
	threads[i].start()

for i in nloops:
	threads[i].join()

print "all end   at: ",ctime()