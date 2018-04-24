# -*- coding: utf-8 -*-

import threading
import time
semaphore = threading.Semaphore(2)


def worker(id):
    print 'thread {id} acquire semaphore'.format(id=id)
    semaphore.acquire()
    print 'thread {id} get semaphore do something'.format(id=id)
    time.sleep(2)
    semaphore.release()
    print 'thread {id} release semaphore'.format(id=id)


if __name__ == '__main__':

    for i in range(10):
        t = threading.Thread(target=worker, args=(i, ))
        t.start()
