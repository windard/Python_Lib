# -*- coding: utf-8 -*-

import time
import random
from multiprocessing import Queue, Process, JoinableQueue, Lock


def writeQ(q):
    for value in ['A', 'B', 'C', 'D', 'E']:
        print 'Put %s to queue ...' % value
        q.put(value)
        time.sleep(random.random())


def readQ(q):
    print 'read q and q status: ', q.empty()
    while not q.empty():
        print 'q is not empty'
        value = q.get()
        print 'Get %s from queue ...' % value
        time.sleep(random.random() * 2)


if __name__ == '__main__':
    q = Queue()
    pw = Process(target=writeQ, args=(q, ))
    pr = Process(target=readQ, args=(q, ))
    pw.start()
    time.sleep(0.001)
    pr.start()
    pw.join()
    pr.join()
