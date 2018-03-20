# coding=utf-8

import time
import gevent
from gevent import  monkey

monkey.patch_all()


def spend_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        rv = func(*args, **kwargs)
        end_time = time.time()
        print end_time - start_time
        return rv
    return wrapper


def daemon():
    time.sleep(1)
    print 'done'


@spend_time
def in_order():
    for i in xrange(3):
        daemon()


@spend_time
def in_concur():
    spawns = []
    for i in xrange(3):
        spawns.append(gevent.spawn(daemon))
    gevent.joinall(spawns)


def main():
    in_order()
    in_concur()


if __name__ == '__main__':
    main()
