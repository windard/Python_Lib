# coding=utf-8

import time
from contextlib import contextmanager

@contextmanager
def reckon_time():
	start = time.time()
	try:
		yield
	finally:
		print "Speeds %f S."%(time.time() - start)

def countsum(count):
	num = 0
	for x in xrange(count):
		num += x
	return num

with reckon_time():
	print countsum(100000)		