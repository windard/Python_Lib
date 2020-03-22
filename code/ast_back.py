# coding=utf-8

import ast
import unparse

code = """
def add(a, b):
	return a + b

print add(1, 2)
"""


class CrazyTransformer(ast.NodeTransformer):

    def visit_BinOp(self, node):
        node.op = ast.Mult()
        return node


def back():
	module = ast.parse(code)
	transformer = CrazyTransformer()
	multi = transformer.visit(module)
	unparse.Unparser(multi)


if __name__ == '__main__':
	back()
