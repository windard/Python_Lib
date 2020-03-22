# coding=utf-8

import ast
import codegen
import astunparse
import astor


code = """
data = {
	"key": "value",
	"list": [1,2,3]
}

def add(a, b):
	return a + b

print add(1, 2)
"""

module = ast.parse(code)

print codegen.to_source(module)
print astunparse.unparse(module)
print astor.to_source(module)
