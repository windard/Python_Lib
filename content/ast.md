## ast

ast 是 python 自带的 语法树生成器，可以用来解析 python 代码，生成抽象语法树。

编译器的编译流程

源代码 --> 语法分析树 (Parse Tree) --> 抽象语法树 (Abstract Syntax Tree) --> 控制流图 (Control Flow Graph) --> 代码对象 (Code Object)

生成抽象语法树的过程就是 ast 实现的过程，我们可以通过 ast 来访问和修改抽象语法树。

### 解析

```
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

```

其实 `ast.parse` 的核心是直接使用 `compile` 编译 

```
def parse(source, filename='<unknown>', mode='exec'):
    """
    Parse the source into an AST node.
    Equivalent to compile(source, filename, mode, PyCF_ONLY_AST).
    """
    return compile(source, filename, mode, PyCF_ONLY_AST)
```

解析生成的结构体有 `_ast.Module`, `_ast.Assign`, `_ast.Str` 等,我们查看 Module 的结构

```
Module(body=[FunctionDef(name='add', args=arguments(args=[Name(id='a', ctx=Param()), Name(id='b', ctx=Param())], vararg=None, kwarg=None, defaults=[]), body=[Return(value=BinOp(left=Name(id='a', ctx=Load()), op=Add(), right=Name(id='b', ctx=Load())))], decorator_list=[]), Expr(value=Call(func=Name(id='add', ctx=Load()), args=[Num(n=1), Num(n=2)], keywords=[], starargs=None, kwargs=None))])
```

我们可以将其中的 加法操作符换成乘法操作符

```
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

```

### 反解析

ast 只管杀不管埋，所以讲抽象语法树再转换为源代码还要我们自己处理一下，也可以用其他的库。

主要有一个 [unparse.py](http://svn.python.org/projects/python/trunk/Demo/parser/unparse.py) 的单文件脚本就可以用。

或者是 `codegen`, `astunparse`, `astor` 等库

```
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

```

还要其他的比如

```
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

```

有一个好消息是 3.9 开始支持 `ast.unparse` 反解析函数。
