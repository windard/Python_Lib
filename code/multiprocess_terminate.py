# -*- coding: utf-8 -*-

import time
import random

from multiprocessing import Queue, Process


def writeQ(q):
    for value in ['A', 'B', 'C', 'D', 'E']:
        print 'Put %s to queue ...' % value
        q.put(value)
        time.sleep(random.random())


def readQ(q):
    while True:
        print 'read q and q status: ', q.empty()
        value = q.get()
        print 'Get %s from queue ...' % value
        time.sleep(random.random() * 2)


if __name__ == '__main__':
    q = Queue()
    q.get()
    pw = Process(target=writeQ, args=(q, ))
    pr = Process(target=readQ, args=(q, ))
    pw.start()
    pr.start()
    pw.join()
    # 死循环，手动终止
    while True:
        if q.empty():
            pr.terminate()
            break
