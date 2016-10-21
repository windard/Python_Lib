#coding=utf-8

import threading
from time import ctime,sleep

def loop(nloop,nsec):
    print "loop",nloop," start at: ",ctime()
    sleep(nsec)
    print "loop",nloop,"end    at: ",ctime()

print "all start at: ",ctime()
loops = [4,2]
threads = []
nloops = range(len(loops))

#创建两个线程
for i in nloops:
    t = threading.Thread(target=loop,args=(i,loops[i]))
    t.setDaemon(False)
    threads.append(t)

#让两个线程同时开始
for i in nloops:
    threads[i].start()

print "all end   at: ",ctime()
