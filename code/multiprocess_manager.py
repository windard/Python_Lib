# -*- coding: utf-8 -*-

import multiprocessing


def func(d, l):
    d[1] = '2'
    d['2'] = 2
    d[0.25] =None
    l.reverse()

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    d = manager.dict()
    l = manager.list(range(10))
    p = multiprocessing.Process(target=func, args=(d, l))
    p.start()
    p.join()

    print(d)
    print(l)
