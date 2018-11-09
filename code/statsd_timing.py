# -*- coding: utf-8 -*-
import time
import random
from statsd import StatsClient
import functools

statsd = StatsClient()


@statsd.timer('myfunc')
def myfunc(a, b):
    statsd.incr("key.incr")
    time.sleep(random.random())


def time_deco(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        statsd.timing('krpc.{}'.format(func.__name__),
                      1000.0 * (time.time() - start_time))
    return wrap


@time_deco
def hello():
    time.sleep(random.random())


if __name__ == '__main__':
    for i in range(100000):
        time.sleep(random.random() / 10)
        # myfunc(1, 1)
        hello()
