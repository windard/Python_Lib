# -*- coding: utf-8 -*-

import os
import time
import random
import threading
# import multiprocessing


class MuProcess(threading.Thread):

    def __init__(self, name):
        super(MuProcess, self).__init__()
        self.name = str(name)

    def run(self):
        print 'Running task %s (%s)' % (self.name, os.getpid())
        start = time.time()
        time.sleep(random.random() * 5)
        end = time.time()
        spend = end - start
        print 'Task %s run %0.2f econds.' % (self.name, spend)
        return spend


if __name__ == '__main__':
    print 'Parent process %s' % os.getpid()

    def callback(*args, **kwargs):
        print 'all process done', args, kwargs

    processes = map(lambda x: MuProcess(x), [i for i in range(10)])
    for p in processes:
        callback(p.start())
    print 'wait for all subprocess done.'
    for p in processes:
        p.join()
    print 'All task done.'
