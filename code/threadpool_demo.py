# -*- coding: utf-8 -*-

import threadpool

import os
import time
import random
import multiprocessing


def long_time_task(name):
    print 'Running task %s (%s)' % (name, os.getpid())
    start = time.time()
    time.sleep(random.random() * 5)
    end = time.time()
    print 'Task %s run %0.2f econds.' % (name, end - start)
    return end - start


if __name__ == '__main__':
    worker = multiprocessing.cpu_count()
    print 'Parent process %s' % os.getpid()
    print 'PC has %s CPU workers' % worker

    def callback(*args, **kwargs):
        print 'all process done', args, kwargs

    names = [i for i in range(10)]
    pool = threadpool.ThreadPool(worker)
    requests = threadpool.makeRequests(long_time_task, names, callback=callback)
    print 'wait for all subprocess done.'
    workers = [pool.putRequest(req) for req in requests]
    print 'task start'
    pool.wait()
    print 'All task done.'
