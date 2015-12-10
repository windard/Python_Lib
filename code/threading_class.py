#coding=utf-8

import threading
from time import ctime,sleep

class ThreadFunc(object):
	def __init__(self, func ,args,name=""):
		self.args = args
		self.func = func
		self.name = name

	def __call__(self):
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
	t = threading.Thread(target=ThreadFunc(loop,(i,loops[i]),loop.__name__))
	threads.append(t)	

for i in nloops:
	threads[i].start()

for i in nloops:
	threads[i].join()

print "all end   at: ",ctime()