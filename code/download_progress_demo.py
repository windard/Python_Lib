# -*- coding: utf-8 -*-
from __future__ import division
import sys
import time

def progress():
    for i in range(100):
        sys.stdout.write("\r[%s%s] %2d%%" % ('█' * i, ' ' * (99 - i), (i / 99) * 100))
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\n')


if __name__ == '__main__':
    progress()
