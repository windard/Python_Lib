## functools

功能类似于 Python 的装饰器，可以用来为函数添加一些新的返回或调用。

#### partial

partial 的源代码，反正我是没看懂

```
def partial(func, *args, **keywords):
    def newfunc(*fargs, **fkeywords):
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords)
        return func(*(args + fargs), **newkeywords) #合并，调用原始函数，此时用了partial的参数
    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc
```

来一个实例就大概明白了，即 Python 偏函数，就是在调用一个函数时总是有相同的参数，就可以将这个相同的参数和这个函数一起提取出来，单独作为一个函数。

其实跟函数的默认值计较类似，不过现在通过偏函数这个新的函数将一个值固定，这次不再是默认值，而是固定值。

```
from functools import partial

basetwo = partial(int, base=2)

basetwo.__doc__ = 'Convert base 2 string to an int.'

basetwo('10010')

def greet(name, year, words):
	print name,year,words

hello=partial(greet, year='2016', words='hello')
hello('foo')

hello=partial(greet, '2016', 'hello')
hello('bar!')

```

将二进制字符串转换为十进制，可以将一个参数固定重新封装成一个函数。

#### update_wrapper

这个函数主要为了解决这样一个问题，在函数解释器中，只要你使用了函数解释器，那么当你想看这个函数的文档和名字时，就会发现你看到的不是这个函数的，而是函数解释器里面的那个函数的。

这个函数的定义有这么长，`update_wrapper(wrapper, wrapped, assigned=('__module__', '__name__', '__doc__'), updated=('__dict__',))`。

```
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

```

运行结果

```
Thu Oct 20 20:54:38 2016
Good Morning
Thu Oct 20 20:54:39 2016
Good Afternon
show the time when func run
getnow
```

函数解释器运行正常，然而最后的函数的文档和名称好像不对的吧，那么如果使用 update_wrapper 来试一下。

```
# coding=utf-8

from time import ctime,sleep
from functools import update_wrapper

def showtime(func):
	def getnow(*args):
		"""show the time when func run """
		print ctime()
		return func(*args)
	return update_wrapper(getnow,func)

@showtime
def greet(now):
	"""greet to others"""
	print "Good "+now

greet("Morning")

sleep(1)

greet("Afternon")

print greet.__doc__
print greet.__name__
```

运行结果

```
Thu Oct 20 20:53:46 2016
Good Morning
Thu Oct 20 20:53:47 2016
Good Afternon
greet to others
greet
```

这次正常了，虽然使用了函数解释器，但是解释器不能喧宾夺主吖，主要的函数名称怎么能错的了呢。

#### wraps

这次就是在函数装饰器里套函数装饰器，使正常的函数装饰器的写法，也能得到上面的效果，在调用时是正常的函数文档和函数名。

同样是一段看不懂的函数定义，`wraps(wrapped, assigned=('__module__', '__name__', '__doc__'), updated=('__dict__',))`。

```
# coding=utf-8

from functools import wraps
from time import ctime,sleep

def showtime(func):
	@wraps(func)
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
```

结果

```
Thu Oct 20 21:24:12 2016
Good Morning
Thu Oct 20 21:24:13 2016
Good Afternon
greet to others
greet
```

#### reduce

好了，复杂难懂的终于结束了，这个的功能就是于内置函数 `reduce` 一致，函数定义也终于能够看懂了，`reduce(function, sequence[, initial])` ，功能是把序列的第一个和第二个元素作为参数传入函数中，然后将得到的结果与第三个元素一起传入函数，然后将得到的结果与第四个元素一起传入函数。。。。一直到与最后一个元素一起传入函数，得到种的结果。 如果 initial 不为 None，则，一开始就是把 init 的值和第一个元素作为参数传入函数，然后一样的依次递归下去。

```
>>> from functools import reduce
>>> reduce(lambda x,y:x+y ,range(5))
10
>>> reduce(lambda x,y:x+y ,range(5),20)
30
>>> from itertools import count,takewhile
>>> reduce(lambda x,y:x+y ,takewhile(lambda x:x < 5 , count()),20)
30
```

#### cmp_to_key

#### total_ordering

两个函数不懂，都不能写一个好好的示例了。


#### 缓存

在 Python 3.2 及以后的版本中，可以使用 `functools.lru_cache` 作为一个简单的函数缓存装饰器

```
# coding=utf-8

from functools import lru_cache


@lru_cache(maxsize=32)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

print([fib(n) for n in range(10)])
# Output: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# 清除缓存
fib.cache_clear()

```

最常见的实现缓存的方法

```
# coding=utf-8

import time


def time_cache(n, saved={}):
    if n in saved:
        return saved[n]
    result = time.time()
    saved[n] = result
    return result

print time_cache(1)
time.sleep(2)
print time_cache(1)
time.sleep(2)
print time_cache(1)

```

或者使用装饰器

```
# coding=utf-8

from functools import wraps
import time


def cache(func):
    saved = {}

    @wraps(func)
    def new_func(*args):
        if args in saved:
            return saved[args]
        result = func(*args)
        saved[args] = result
        return result
    return new_func

@cache
def test_cache(n):
    return time.time()

print test_cache(1)
time.sleep(3)
print test_cache(1)
time.sleep(3)
print test_cache(1)

```

在使用装饰器实现缓存的时候很容易理解，在装饰器内有一个闭包，闭包中的变量一直保存。但是在没有装饰器的实现中，如果没有使用全局变量的话，为什么一个默认参数会被一直保存。

这是 Python 的 默认参数陷阱，每一个 Python 的默认参数在第一次编译执行之后都会保留，在下次执行调用时使用同样的参数。

使用相同参数的情况在不可变对象中也会出现，只不过因为不可变对象的值并不会造成影响，所以没有引起注意。

> Default values are computed once, then re-used.

默认参数陷阱的典型场景 

```
# coding=utf-8

def foo(x=[]):
    x.append(1)
    print x

foo()
foo()
foo()
foo()

```

结果是

```
[1]
[1, 1]
[1, 1, 1]
[1, 1, 1, 1]
```

如果想要正常的结果只能

```
# coding=utf-8

def foo(x=[]):
    x.append(1)
    print x

foo(x=[])
foo(x=[])
foo(x=[])
foo(x=[])
foo(x=[])

```

或者

```
# coding=utf-8

def foo(x=None):
    if not x:
        x = []
    x.append(1)
    print x

foo()
foo()
foo()
foo()
foo()

```

在使用时注意即可，当然这种陷阱也并非全不好处，像缓存操作即是使用其利处的一面。

#### 参考链接

[PYTHON-进阶-FUNCTOOLS模块小结](http://www.wklken.me/posts/2013/08/18/python-extra-functools.html)

[Higher-order functions and operations on callable objects](https://docs.python.org/2/library/functools.html)
