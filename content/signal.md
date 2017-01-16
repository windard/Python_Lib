## signal

信号量模块，一般信号量的操作用来解决同步与异步的问题，避免死锁。同样的，Windows 下的功能不齐全，最好在 Linux 下。

```
# coding=utf-8

import time
import signal

def handle(signo, frame):
	print "Got Signal",signo

signal.signal(signal.SIGINT, handle)

# Unix Only
signal.alarm(2)

now = time.now()

time.sleep(200)

print "sleep for",time.time() - now," seconds "

```