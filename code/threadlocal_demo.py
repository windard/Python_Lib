# -*- coding: utf-8 -*-

import threading


local = threading.local()


def process_name():
    print "hello %s, in %s" % (local.name, threading.current_thread().name)


def process_local(name):
    local.name = name
    process_name()


if __name__ == '__main__':
    local.name = 'Cli'
    process_name()
    t1 = threading.Thread(target=process_local, args=('Bob', ), name='Target-A')  # noqa
    t2 = threading.Thread(target=process_local, args=('Alice', ), name='Target-B')  # noqa

    t1.start()
    t2.start()

    t1.join()
    t2.join()
