# coding=utf-8

import ast


code = """
def add(a, b):
	return a + b

print add(1, 2)
"""


class CrazyTransformer(ast.NodeTransformer):

    def visit_BinOp(self, node):
        print node.__dict__
        node.op = ast.Mult()
        print node.__dict__
        return node


def main():
	module = ast.parse(code)
	exec compile(module, '<string>', 'exec')
	transformer = CrazyTransformer()
	multi = transformer.visit(module)
	exec compile(multi, '<string>', 'exec')


if __name__ == '__main__':
	main()
