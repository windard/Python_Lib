# coding=utf-8
# 只能这里么？


# fist two line comment
# 再来一行注释

functions = {}

def add(a, b):
	return a + b


class A(object):
	"""
	A class
	"""
	def ___init__(self, name):
		self.name = name


class B(A):
	
	def hello(self, word=None):
		"""
		greeting
		"""
		if not word:
			word = self.name
		print "hello {}".format(word)


a = A()
b = B()
