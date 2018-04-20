# -*- coding: utf-8 -*-

import os
import time
import multiprocessing

def multi(x):
    return x + 42


if __name__ == '__main__':
    pool = multiprocessing.Pool()

    print pool.map(multi, range(10))
    print pool.map_async(multi, range(10)).get()

    for i in pool.imap_unordered(multi, range(10)):
        print i,

    print
    res = pool.apply_async(multi, (20, ))
    print res.get(timeout=20)

    res = pool.apply_async(os.getpid)
    print res.get()

    multiple_results = [pool.apply_async(os.getpid) for _ in range(4)]
    print [res.get() for res in multiple_results]

    res = pool.apply_async(time.sleep, (10, ))
    try:
        print res.get(timeout=1)
    except multiprocessing.TimeoutError:
        print 'we lacked patience and got a timeout error'
