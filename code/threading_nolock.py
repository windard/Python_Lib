#coding=utf-8

import threading
from time import ctime,sleep

counter = 0

class MyThread1(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		global counter
		counter += 1
		print "  "+str(counter)+"  "

class MyThread2(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		global counter
		counter -= 1
		print "  "+str(counter)+"  "

if __name__ == '__main__':
	threads = []
	for i in range(20):
		if i%2:
			t = MyThread1()
		else:
			t = MyThread2()
		threads.append(t)

	for t in threads:
		t.start()