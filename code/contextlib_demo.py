# coding=utf-8

from contextlib import contextmanager

@contextmanager
def make_open_context(filename, mode):
	fp = open(filename, mode=mode)
	try:
		yield fp
	finally:
		fp.close()

with make_open_context("/tmp/a", "a") as f:
	f.write("hello wordl !")