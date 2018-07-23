# -*- coding: utf-8 -*-

import os
import signal

# 定义一个信号处理函数，该函数打印收到的信号，然后raise IOError
def handler(signum, frame):
    print 'Signal handler called with signal', signum
    raise IOError("Couldn't open device!")

# 对SIGALRM(终止)设置处理的handler, 然后设置定时器，5秒后触发SIGALRM信号
signal.signal(signal.SIGALRM, handler)
signal.alarm(5)

# open 操作可能异常等待
fd = os.open('/dev/ttys0', os.O_RDWR)

signal.alarm(0)          # 关闭定时器
