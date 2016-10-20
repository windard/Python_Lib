# coding=utf-8

from time import ctime,sleep
from functools import update_wrapper

def showtime(func):
	def getnow(*args):
		"""show the time when func run """
		print ctime()
		return func(*args)
	return update_wrapper(getnow,func)

@showtime
def greet(now):
	"""greet to others"""
	print "Good "+now

greet("Morning")

sleep(1)

greet("Afternon")

print greet.__doc__
print greet.__name__