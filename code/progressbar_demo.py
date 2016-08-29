# coding=utf-8

from __future__ import division
import math
import time
import sys
 
def progressbar(cur, total):
    percent = '{:.2%}'.format(cur / total)
    sys.stdout.write('\r')
    sys.stdout.write("[%-50s] %s" % (
                            '=' * int(math.floor(cur * 50 / total)),
                            percent))
    sys.stdout.flush()

t = 0
while t < 9.9:
	t += 0.1
	time.sleep(0.1)
	progressbar(t,10)
print
