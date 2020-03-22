## inspect

inspect 提供更为强大的 python 自省功能。

### 自查

#### 检查模块

查看模块中的所有内容

example.py

```
# coding=utf-8

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


```

```
# coding=utf-8

import inspect

import example


def detect_all():
    for name, data in inspect.getmembers(example):
        if name.startswith('__'):
            continue
        print('{} : {}'.format(name, data))


def detect_class():
    for name, data in inspect.getmembers(example, inspect.isclass):
        if name.startswith('__'):
            continue
        print('{} : {}'.format(name, data))


def detect_code():
    for name, data in inspect.getmembers(example, inspect.iscode):
        if name.startswith('__'):
            continue
        print('{} : {}'.format(name, data))


def detect_function():
    for name, data in inspect.getmembers(example, inspect.isfunction):
        if name.startswith('__'):
            continue
        print('{} : {}'.format(name, data))


if __name__ == '__main__':
    print "all:"
    detect_all()
    print "class:"
    detect_class()
    print "function:"
    detect_function()
    print "code:"
    detect_code()

```

然后即可得到 example 中的模块数据

```
A : <class 'example.A'>
B : <class 'example.B'>
a : <example.A object at 0x101e65550>
add : <function add at 0x101e4d7d0>
b : <example.B object at 0x101e65590>
functions : {}
```

#### 检查类和实例

实际上 `inspect.getmembers` 不但能检查模块，还能检查类和实例，其功能类似于 `dir(obj)` 但是会返回更加详细内容。
> 😂，好吧，其实内部就是调用 `dir` 的功能，只不过加了一个筛选和排序的功能。

```
# coding=utf-8

import inspect
import example


def detect_class():
    print("A:")
    for name, data in inspect.getmembers(example.A):
        print('{} : {}'.format(name, data))


def detect_method():
    print("A:")
    for name, data in inspect.getmembers(example.A, inspect.ismethod):
        print('{} : {}'.format(name, data))
    print("B:")
    for name, data in inspect.getmembers(example.B, inspect.ismethod):
        print('{} : {}'.format(name, data))
    print("a:")
    for name, data in inspect.getmembers(example.a, inspect.ismethod):
        print('{} : {}'.format(name, data))


if __name__ == '__main__':
    detect_class()
    detect_method()

```

然后我们可以发现，其实主要的功能在 inspect 提供了大量的 isXXX 函数，可以用来审查判断类型。

```
# coding=utf-8

import inspect
import example

if __name__ == '__main__':
    print inspect.isbuiltin(apply)
    print inspect.isbuiltin(lambda: None)
    print inspect.isclass(type)
    print inspect.isclass(1)
    print inspect.iscode(example.add.func_code)
    print inspect.iscode(example.B.hello.im_func.func_code)
    print inspect.iscode("1+1")
    print inspect.ismodule(inspect)
    print inspect.isfunction(input)
    print inspect.isgenerator(iter([]))
    print inspect.isgenerator([])

```

还有其他的一些有趣的功能，比如提取注释，文档和源代码。

注释的话，只能提取第一部分，即以空行分割之后则不会输出。文档的话，会比使用 `__doc__` 更加漂亮的格式输出，源代码的话，其实是从文件中再次读取出来的。

```
# coding=utf-8

import inspect
import example

if __name__ == '__main__':

    print inspect.getcomments(example)
    print inspect.getdoc(example)
    print inspect.getdoc(example.A)
    print inspect.getdoc(example.B.hello)

    print inspect.findsource(example.A)

    print inspect.getabsfile(example.A)
    print inspect.getfile(example.A)
    print inspect.getsource(example)
    print inspect.getsource(example.A)
    print inspect.getsourcefile(example.A)
    print inspect.getsourcelines(example.A)

    print inspect.getmodule(example.A)
    print inspect.getmoduleinfo("example.py")
    print inspect.getmodulename("example.py")

```

#### 获取函数参数

```
# coding=utf-8

import inspect
import example


def main(a=1):
    print inspect.getargvalues(inspect.currentframe())


if __name__ == '__main__':
    main()
    print inspect.getargspec(example.add)
    print inspect.formatargspec(inspect.getargspec(example.add))
    print inspect.getargspec(example.B.hello)
    print inspect.getcallargs(example.add, 1, 2)
    print inspect.getcallargs(example.B.hello, self=None, word="world")

```

获取当前请求参数和指定函数参数和参数组装。

#### 获取堆栈信息

栈是用来展示调用链路，每一层都是一个帧

帧是当前的上下文，调用时的环境变量和数据

```
# coding=utf-8

import inspect


def get_frame():
    """
    帧是当前的上下文，调用时的环境变量和数据
    """
    frame = inspect.currentframe()
    print 'line {} of {}'.format(frame.f_lineno, frame.f_code.co_filename)
    print 'locals: {}'.format(frame.f_locals)


def get_stack():
    """
    栈是用来展示调用链路，每一层都是一个帧
    """
    for frame, filename, lineno, func, code_context, code_index in inspect.stack():
        print('{}[{}]\n -> {}:{}'.format(
            filename,
            lineno,
            func,
            code_context[code_index].strip()
        ))
        print frame.f_locals


if __name__ == '__main__':
    frame = inspect.currentframe()
    print 'line {} of {}'.format(frame.f_lineno, frame.f_code.co_filename)
    print 'locals: {}'.format(frame.f_locals)

    get_frame()
    get_stack()

```

### 源码
在查看 inspect 源代码后可以对 inspect 函数库有更深入的理解，inspect 为单文件库，以一串中横线分割，整个代码分为六个部分。

分别为
- type-checking 				类型检查
- class helpers 				类帮助
- source code extraction 		源代码提取
- class tree extraction 		类层次结构
- argument list extraction 		参数列表提取
- stack frame extraction 		栈帧提取

而每个部分提供不同的功能

#### 类型检查

- ismodule
- isclass
- ismethod
- ismethoddescriptor
- isdatadescriptor
- ismemberdescriptor
- isgetsetdescriptor
- isfunction
- isgeneratorfunction
- isgenerator
- istraceback
- isframe
- iscode
- isbuiltin
- isroutine 是否是常规函数，其可能是 method ，可能是 function ，可能是 builtin ，可能是 methoddescriptor
- isabstract
- getmembers
- classify_class_attrs 将 getmembers 的结果以 Attribute 类的形式返回列表，主要有 name kind defining_class object 四个字段

一般的子类收集或者函数收集的时候通用的两种方式，一种是自省查找，一种是自动注册。在 Java 的依赖注入或者 python 中都有用到。

#### 类帮助

- getmro 这个就很简单，查看类的 MRO 信息

#### 源代码提取
- getdoc
- getfile
- getmoduleinfo
- getmodulename
- getsourcefile
- getabsfile
- getmodule
- findsource
- getcomments
- getblock
- getsourcelines
- getsource

#### 类层次结构

- getclasstree 输入多个类，输出其继承依赖关系

#### 参数列表提取

- getargspec
- getargvalues
- getcallargs
- formatargspec
- formatargvalues

#### 栈帧提取

- stack
- currentframe
- trace
- getouterframes
- getinnerframes
