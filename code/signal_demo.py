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
