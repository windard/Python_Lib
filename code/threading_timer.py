# -*- coding: utf-8 -*-
import time
import threading


def on_timer():
    print time.time()
    set_timer()


def set_timer():
    _timer = threading.Timer(10, on_timer)
    _timer.start()


set_timer()
while 1:
    time.sleep(5)
    print 'sleep', time.time()
