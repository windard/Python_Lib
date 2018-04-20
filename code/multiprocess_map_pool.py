# -*- coding: utf-8 -*-

import os
import time
import random
import multiprocessing


def long_time_task(name):
    print 'Running task %s (%s)' % (name, os.getpid())
    start = time.time()
    time.sleep(random.random() * 5)
    end = time.time()
    spend = end - start
    print 'Task %s run %0.2f econds.' % (name, spend)
    return spend


if __name__ == '__main__':
    worker = multiprocessing.cpu_count()
    print 'Parent process %s' % os.getpid()
    print 'PC has %s CPU workers' % worker
    p = multiprocessing.Pool(worker)

    def callback(*args, **kwargs):
        print 'all process done', args, kwargs

    names = [i for i in range(10)]
    p.map_async(long_time_task, names, callback=callback)
    print 'wait for all subprocess done.'
    p.close()
    print 'task start'
    p.join()
    print 'All task done.'
