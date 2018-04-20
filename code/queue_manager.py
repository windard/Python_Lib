# -*- coding: utf-8 -*-

import random
import Queue

from multiprocessing.managers import BaseManager


class QueueManager(BaseManager):
    pass


if __name__ == '__main__':

    task_queue = Queue.Queue()
    result_queue = Queue.Queue()


    QueueManager.register('get_task_queue', callable=lambda :task_queue)
    QueueManager.register('get_result_queue', callable=lambda :result_queue)

    manager = QueueManager(address=('', 5000), authkey='abc')

    manager.start()


    task = manager.get_task_queue()
    result = manager.get_result_queue()

    for i in range(10):
        n = random.randrange(100)
        print 'put task %s ...' % n
        task.put(n)

    print 'try get result ...'

    for i in range(10):
        r = result.get(timeout=10)
        print 'result is %s' % r

    manager.shutdown()
