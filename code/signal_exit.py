# -*- coding: utf-8 -*-

import signal
import os


def do_exit(sig, stack):
    raise SystemExit('Exiting')


signal.signal(signal.SIGINT, signal.SIG_IGN)
signal.signal(signal.SIGUSR1, do_exit)

print 'My PID:', os.getpid()

signal.pause()  # 当接受到键盘的时候，signal.SIG_IGN给忽略了
print 'End of Exit'
