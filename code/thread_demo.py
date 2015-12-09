#coding=utf-8

import thread
from time import ctime,sleep

#这次两个函数只用一个函数体,在函数结束后释放这个锁
def loop(nloop,nsec,lock):
	print "loop",nloop," start at: ",ctime()
	sleep(nsec)
	print "loop",nloop,"end    at: ",ctime()
	lock.release()

print "all start at: ",ctime()
#两个函数运行时间
loops = [4,2]
#这是两个锁的列表
locks = []
nloops = range(len(loops))

#创建两个锁
for i in nloops:
	lock = thread.allocate_lock()
	lock.acquire()
	locks.append(lock)

#创建两个带锁的线程
for i in nloops:
	thread.start_new_thread(loop,(i,loops[i],locks[i]))

#等待两个带锁的线程结束
for i in nloops:
	while locks[i].locked():
		pass

print "all end   at: ",ctime()