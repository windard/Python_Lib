# -*- coding: utf-8 -*-
from multiprocessing import Process, Manager, Lock
import os


manager = Manager()
sum = manager.Value('tmp', 0)
lock = Lock()


def testFunc(cc):
    # with lock:
    #     sum.value += cc
    sum.value += cc


if __name__ == '__main__':
    ps = []

    for ll in range(100):
        t = Process(target=testFunc, args=(1,))
        ps.append(t)

    for i in range(len(ps)):
        ps[i].start()

    for j in range(len(ps)):
        ps[j].join()

    print "------------------------"
    print 'process id:', os.getpid()
    print sum.value
