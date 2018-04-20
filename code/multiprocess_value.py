# -*- coding: utf-8 -*-

from multiprocessing import Process


def change_global():
    global a
    a.append(1)
    print 'in global', a


def change_local(b):
    b.append(2)
    print 'in local', b


if __name__ == '__main__':
    a = []
    pg = Process(target=change_global)
    pg.start()
    pg.join()
    print a

    pl = Process(target=change_local, args=(a, ))
    pl.start()
    pl.join()
    print a
