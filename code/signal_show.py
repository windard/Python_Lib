# -*- coding: utf-8 -*-

import signal
import os
import time


def receive_signal(signum, stack):
    print 'Received:', signum


def receive_exit(signum, stack):
    print 'Exit'
    raise SystemExit('Exiting')


if __name__ == '__main__':

    # Register signal handlers
    signal.signal(signal.SIGINT, receive_signal)
    signal.signal(signal.SIGQUIT, receive_signal)

    # SIGSTOP, SIGKILL can't received message
    # signal.signal(signal.SIGSTOP, receive_signal)
    # signal.signal(signal.SIGKILL, receive_exit)

    print 'My PID is:', os.getpid()

    while True:
        print 'Waiting...'
        time.sleep(3)
