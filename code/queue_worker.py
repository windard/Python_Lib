# -*- coding: utf-8 -*-

import time
import Queue

from multiprocessing.managers import BaseManager


class QueueManager(BaseManager):
    pass


if __name__ == '__main__':

    QueueManager.register('get_task_queue')
    QueueManager.register('get_result_queue')

    server_addr = ('127.0.0.1', 5000)

    print 'connect to server %s:%d ...' % server_addr

    m = QueueManager(address=server_addr, authkey='abc')
    m.connect()

    task = m.get_task_queue()
    result = m.get_result_queue()


    for i in range(10):
        try:
            n = task.get(timeout=1)
            print 'run task %d * %d' % (n, n)
            r = '%d * %d = %d' % (n, n, n * n)
            time.sleep(n * 0.1)
            result.put(r)
        except Queue.Empty:
            print 'task queue is empty'

    print 'worker exit.'
