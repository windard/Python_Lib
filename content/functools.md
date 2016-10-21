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

def fun(name,greet):
	print name,year,words

hello=partial(greet,year=' 2016 ',words=' hello')

hello('foo')

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

#### 参考链接

[PYTHON-进阶-FUNCTOOLS模块小结](http://www.wklken.me/posts/2013/08/18/python-extra-functools.html)

[Higher-order functions and operations on callable objects](https://docs.python.org/2/library/functools.html)
