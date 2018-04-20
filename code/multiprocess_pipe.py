# -*- coding: utf-8 -*-

import time
import random

from multiprocessing import Process, Pipe, Lock

l = Lock()


def writeQ(q):
    for value in ['A', 'B', 'C', 'D', 'E']:
        print 'Put %s to queue ...' % value
        q.send(value)
        time.sleep(random.random())


def readQ(q):
    for _ in range(2):
        l.acquire()
        print 'read q and q status: ', q.recv()
        l.release()


if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    pw = Process(target=writeQ, args=(child_conn, ))
    pr = Process(target=readQ, args=(parent_conn, ))
    pt = Process(target=readQ, args=(parent_conn, ))
    pw.start()
    pr.start()
    pt.start()

    # print 'from parent', parent_conn.recv()
    # child_conn.send('in parent')
    # child_conn.send('in parent')
    # print 'after parent', parent_conn.recv()

    pw.join()
    pr.join()
    pt.join()
