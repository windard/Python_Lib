# -*- coding: utf-8 -*-

import time
import random


from Queue import Queue
from multiprocessing import Process
from threading import Lock

mux = Lock()
q = Queue()
q.qsize()


def writeQ():
    global q
    for value in ['A', 'B', 'C', 'D', 'E']:
        print 'Put %s to queue ...' % value
        # if mux.acquire():
        q.put(value)
        # mux.release()
        time.sleep(random.random())


def readQ():
    global q
    while True:
        print 'read q and q status: ', q.empty()
        # if mux.acquire():
        value = q.get()
        # mux.release()
        print 'Get %s from queue ...' % value
        time.sleep(random.random() * 2)


if __name__ == '__main__':
    # q.get()
    pw = Process(target=writeQ)
    pr = Process(target=readQ)
    pw.start()
    pw.is_alive()
    pr.start()
    pw.join()
    print 'terminate q', q.qsize()
    # 死循环，手动终止
    while True:
        if q.empty():
            pr.terminate()
            break
