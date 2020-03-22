# coding=utf-8

import ast

code = """
def add(a, b):
	return a + b

add(1, 2)
"""

print "hello world"
print ast.parse(code)
print ast.dump(ast.parse(code))
