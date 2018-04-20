# -*- coding: utf-8 -*-

import os
import time
import random
import multiprocessing
from multiprocessing.pool import ThreadPool


def long_time_task(name):
    print 'Running task %s (%s)' % (name, os.getpid())
    start = time.time()
    time.sleep(random.random() * 5)
    end = time.time()
    print 'Task %s run %0.2f econds.' % (name, end - start)


if __name__ == '__main__':
    worker = multiprocessing.cpu_count()
    print 'Parent process %s' % os.getpid()
    print 'PC has %s CPU workers' % worker
    # p = multiprocessing.Pool(worker)
    p = ThreadPool()

    for i in range(10):
        p.apply_async(long_time_task, (i, ))
    print 'wait for all subprocess done.'
    p.close()
    print 'task start'
    p.join()
    print 'All task done.'
