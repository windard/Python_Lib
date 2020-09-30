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

有一个好消息是 Python 3.9 开始支持 `ast.unparse` 反解析函数。

### 安全的执行

在 Python 中有 `eval` 方法,但是一般如果直接调用 `eval` 执行的话，会有安全风险，可以试下 `ast.literal_eval` 进行安全的代码执行。

这个代码执行可以厉害了`୧(๑•̀◡•́๑)૭ `， 只能含有 Python 基本数据类型，数字，字符串，列表，字典，元组，布尔值，`None` 和复数。
> 😂，复数？是不是突然觉得很突然，为什么会有复数？你是不是已经把复数是啥给忘了？`1+2j` 就是复数。

```python
def literal_eval(node_or_string):
    """
    Safely evaluate an expression node or a string containing a Python
    expression.  The string or node provided may only consist of the following
    Python literal structures: strings, numbers, tuples, lists, dicts, booleans,
    and None.
    """
    _safe_names = {'None': None, 'True': True, 'False': False}
    if isinstance(node_or_string, basestring):
        node_or_string = parse(node_or_string, mode='eval')
    if isinstance(node_or_string, Expression):
        node_or_string = node_or_string.body
    def _convert(node):
        if isinstance(node, Str):
            return node.s
        elif isinstance(node, Num):
            return node.n
        elif isinstance(node, Tuple):
            return tuple(map(_convert, node.elts))
        elif isinstance(node, List):
            return list(map(_convert, node.elts))
        elif isinstance(node, Dict):
            return dict((_convert(k), _convert(v)) for k, v
                        in zip(node.keys, node.values))
        elif isinstance(node, Name):
            if node.id in _safe_names:
                return _safe_names[node.id]
        elif isinstance(node, BinOp) and \
             isinstance(node.op, (Add, Sub)) and \
             isinstance(node.right, Num) and \
             isinstance(node.right.n, complex) and \
             isinstance(node.left, Num) and \
             isinstance(node.left.n, (int, long, float)):
            left = node.left.n
            right = node.right.n
            if isinstance(node.op, Add):
                return left + right
            else:
                return left - right
        raise ValueError('malformed string')
    return _convert(node_or_string)
```

源码很简单，可以直接看代码，或者手动测试。

赋值操作不能用，加减乘除不能用，比较运算不能用，连集合都不能用。复数可以用，负数也可以，但是正数就不行。
> 好消息是从 Python 3.2 开始支持集合。

```python
# -*- coding: utf-8 -*-

import ast


if __name__ == '__main__':
    # 赋值操作不能有
    # print ast.literal_eval("a=1")
    # print eval("a=1")
    # a = 1
    # 加减乘除都不能有
    # print ast.literal_eval("1+1")
    # print eval("1+1")
    # print ast.literal_eval("1==1")
    print eval("1==1")
    print ast.literal_eval("1")
    print ast.literal_eval("None")
    # 连集合都不能有
    # print ast.literal_eval("{1,2,4}")
    # print ast.literal_eval("set([1])")
    # print ast.literal_eval("[1,2,{'1', 2, '2,3,4'}, [4,5,'6']]")
    # print [1,2,{'1', 2, '2,3,4'}, [4,5,'6']]
    print ast.literal_eval("[1,2,3,{2:3}]")
    # 连最终结果是一个list也不行
    # print ast.literal_eval("list([1,2,3])")
    print list([1, 2, 3])
    # print ast.literal_eval("[1,2+3]")
    # 复数可以有，负数也可以有
    print ast.literal_eval("1+2j")
    print ast.literal_eval("-2")
    # print ast.literal_eval("--2")
    # 正数就不行
    # print ast.literal_eval("+2")
    # print ast.literal_eval("++2")

```

