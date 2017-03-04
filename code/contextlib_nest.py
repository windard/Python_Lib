# coding=utf-8

from contextlib import contextmanager

@contextmanager
def make_context(*args):
	print args
	yield

with make_context(1, 2):
	with make_context(3, 4):
		print "in the context"

with make_context(1, 2) , make_context(3, 4):
	print "in the context"

# if python < 2.7

from contextlib import nested

with nested(make_context(1, 2), make_context(3, 4)):
	print "in the context"