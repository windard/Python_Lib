## contextlib

上下文管理器让代码可读性更强，并且错误更少。几个典型的应用场景在文件打开自动关闭，线程锁获取自动释放，数据库钩子获取自动释放等地方。

如线程锁获取自动释放的实现，和文打开自动关闭的上下文管理器

```
# coding=utf-8

import threading

class LockContext(object):
    """docstring for LockContext"""
    def __init__(self):
        print "__init__"
        self.lock = threading.Lock()

    def __enter__(self):
        print "__enter__"
        self.lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print "__exit__"
        self.lock.release()

with LockContext():
    print "in the context"

class OpenContext(object):
    """docstring for OpenContext"""
    def __init__(self, filename, mode):
        self.fp = open(filename, mode)

    def __enter__(self):
        return self.fp

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fp.close()

with OpenContext("/tmp/a", "a") as f:
    f.write("hello world ~ ")

```

如果手动构造上下文管理器的话比较复杂，需要实现 `__enter__` 和 `__exit__` 方法，如实现一个计算程序运行时间的管理器。

```
# coding=utf-8
import time

class ElapsedTime(object):
    def __enter__(self):
        self.start_time = time.time()
    def __exit__(self, exception_type, exception_value, traceback):
        self.end_time = time.time()
        print "Speeds %f S."%(self.end_time - self.start_time)

def countsum(count):
    num = 0
    for x in xrange(count):
        num += x
    return num

with ElapsedTime():
    print countsum(100000)
```

或者使用装饰器实现

```
# coding=utf-8

import time

def ElapsedTimeWarp(func):
    def spendtime(*args, **kwargs):
        start_time = time.clock()
        result = func(*args, **kwargs)
        end_time = time.clock()
        print "Speeds %f S." % (end_time - start_time)
        return result
    return spendtime

@ElapsedTimeWarp
def countsum(count):
    num = 0
    for x in xrange(count):
        num += x
    return num

print countsum(100000)
```

或者使用闭包函数的写法

```
# coding=utf-8
import time

def ElapsedTimeWarp(func):
    def spendtime(*args, **kwargs):
        start_time = time.clock()
        result = func(*args, **kwargs)
        end_time = time.clock()
        print "Speeds %f S." % (end_time - start_time)
        return result
    return spendtime

def countsum(count):
    num = 0
    for x in xrange(count):
        num += x
    return num

print ElapsedTimeWarp(countsum)(100000)

```

使用 contextlib 可以让上下文生成器更简单。

```
# coding=utf-8

from contextlib import contextmanager

@contextmanager
def make_open_context(filename, mode):
    fp = open(filename, mode=mode)
    try:
        yield fp
    finally:
        fp.close()

with make_open_context("/tmp/a", "a") as f:
    f.write("hello wordl !")
```

如果使用 协程 的话，还可以更简单

```
# coding=utf-8

from contextlib import contextmanager


@contextmanager
def open_file(name, mode='r'):
    f = open(name, mode)
    yield f
    f.close()

with open_file("./contextlib_file.py") as f:
    for i in f:
        print i,

```

还有我们的时间管理器

```
# coding=utf-8

import time
from contextlib import contextmanager

@contextmanager
def reckon_time():
    start = time.time()
    try:
        yield
    finally:
        print "Speeds %f S."%(time.time() - start)

def countsum(count):
    num = 0
    for x in xrange(count):
        num += x
    return num

with reckon_time():
    print countsum(100000)
```

或者是用来忽略异常

```
@contextlib.contextmanager
def ignore_errors(*errors):
    if not errors:
        errors = Exception
    try:
        yield
    except errors:
        pass

```

如果有多个上下文嵌套的话，可以使用双重 with 语句，或者 with 语句并列。如果 Python 版本小于 2.7 则需要使用 `contextlib.nested` 来减少 with 的嵌套

```
# coding=utf-8

from contextlib import contextmanager

@contextmanager
def make_context(*args):
    print args
    yield

with make_context(1, 2):
    with make_context(3, 4):
        print "in the context"

with make_context(1, 2) , make_context(3, 4):
    print "in the context"

# if python < 2.7

from contextlib import nested

with nested(make_context(1, 2), make_context(3, 4)):
    print "in the context"
```