# coding=utf-8

import select
import sys

while True:
    readable, writeable, error = select.select([sys.stdin, ], [], [])
    if sys.stdin in readable:
        print 'select get stdin:', sys.stdin.readline(),
