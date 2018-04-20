# -*- coding: utf-8 -*-

import threading
from Queue import Queue
from random import randrange
from time import sleep


class Worker(threading.Thread):

    def __init__(self, tasks):
        super(Worker, self).__init__()
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kwargs = self.tasks.get()
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(e)
            finally:
                self.tasks.task_done()


class ThreadPool(object):
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in xrange(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kwargs):
        self.tasks.put((func, args, kwargs))

    def map(self, func, args_list):
        for args in args_list:
            self.add_task(func, args)

    def wait_completion(self):
        self.tasks.join()


if __name__ == '__main__':
    def wait_delay(d):
        print('sleep for (%d)sec' % d)
        sleep(d)


    delays = [randrange(3, 7) for i in range(50)]
    pool = ThreadPool(5)

    pool.map(wait_delay, delays)
    pool.wait_completion()
