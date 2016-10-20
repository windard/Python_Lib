# coding=utf-8

from time import ctime,sleep

def showtime(func):
	def getnow(*args):
		"""show the time when func run """
		print ctime()
		return func(*args)
	return getnow

@showtime
def greet(now):
	"""greet to others"""
	print "Good "+now

greet("Morning")

sleep(1)

greet("Afternon")

print greet.__doc__
print greet.__name__