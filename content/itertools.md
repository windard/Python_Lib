## itertools

### 迭代器

迭代器 (iterator) 是可迭代对象的一种。

在设计到大量数据的计算的时候，如果这些数据不是并行计算的，那么我们一般不会一开始就将大量数据加载到内存中，而是边加载边计算，这样可以节省内存空间，加快运算速率。同样的，在 Python 科学计算中，我们在遇到大量数据时也不用同时将大量数据同时加载到 数组 中，而是可以使用一个迭代器，每次返回数组的一个值，关于这个值的计算结束后，我们再加载下一个数据。

这样的数组对象我们称之为 迭代器，在使用时与一般数组对象无异，但是其实在计算时却可以节省内存空间，加快运算速率。

一般常见的循环对象有 open 文件之后打开的文件对象，使用 next 方法读取下一行数据，直到遇到 StopIteration 异常，结束读取。

```
f = open('text.txt')

print f.next()
print f.next()
print f.next()

for x in f:
	print x
```

除了 文件操作符 这个迭代器之外，我们也可以使用 `iter` 方法，将集合数据类型的可迭代对象转换为 迭代器对象。

```
>>> a = [1,2,3,4,5]
>>> b=iter(a)
>>> b
<listiterator object at 0x0298D970>
>>> b.next()
1
>>> b.next()
2
>>> for x in b:
...     print x
...
3
4
5
>>> b.next()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

### 生成器

生成器 (generator) 一般是由 yield 生成的循环对象，生成器也是迭代器的一种。

生成器的编写与一般的函数类似，不过在 return 的地方改为 yield 。在生成器中可以有多个 yield ，当生成器遇到一个 yield 的时候会暂停运行生成器，返回 yield 值，当再次调用生成器的时候，会从上次暂停的地方继续运行，直到下一个 yield 。

```
>>> def gen():
...     yield 1
...     for x in xrange(6):
...             yield(x)
...
>>> c = gen()
>>> c
<generator object gen at 0x024BDEE0>
>>> c.next()
1
>>> c.next()
0
>>> for x in c:
...     print x
...
1
2
3
4
5
>>> c.next()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

每一次调用生成器返回一个 yield 值，并在返回处暂停，下次继续从暂停处开始执行。

### itertools

由名字可以看出这个 标准库 是与 生成器 有关的，它包含了很多更加有效的生成器工具。

```
	Functional tools for creating and using iterators.

	Infinite iterators:
    count([n]) --> n, n+1, n+2, ...
    cycle(p) --> p0, p1, ... plast, p0, p1, ...
    repeat(elem [,n]) --> elem, elem, elem, ... endlessly or up to n times

    Iterators terminating on the shortest input sequence:
    chain(p, q, ...) --> p0, p1, ... plast, q0, q1, ...
    compress(data, selectors) --> (d[0] if s[0]), (d[1] if s[1]), ...
    dropwhile(pred, seq) --> seq[n], seq[n+1], starting when pred fails
    groupby(iterable[, keyfunc]) --> sub-iterators grouped by value of keyfunc(v)
    ifilter(pred, seq) --> elements of seq where pred(elem) is True
    ifilterfalse(pred, seq) --> elements of seq where pred(elem) is False
    islice(seq, [start,] stop [, step]) --> elements from
           seq[start:stop:step]
    imap(fun, p, q, ...) --> fun(p0, q0), fun(p1, q1), ...
    starmap(fun, seq) --> fun(*seq[0]), fun(*seq[1]), ...
    tee(it, n=2) --> (it1, it2 , ... itn) splits one iterator into n
    takewhile(pred, seq) --> seq[0], seq[1], until pred fails
    izip(p, q, ...) --> (p[0], q[0]), (p[1], q[1]), ...
    izip_longest(p, q, ...) --> (p[0], q[0]), (p[1], q[1]), ...

    Combinatoric generators:
    product(p, q, ... [repeat=1]) --> cartesian product
    permutations(p[, r])
    combinations(p, r)
    combinations_with_replacement(p, r)

```

我们来试一下

##### 无穷循环器

- count([a=0[,b=1]]) 从 a 开始 依次累加 b ,如 count(5,2) 得到 5,7,9,11...
- cycle(p) 依次循环输出 p0,p1...pn,p0,p1...,如 count('abc') 得到 a,b,c,a,b...
- repeat(e[,n]) 循环一直输出 e 无穷次或 n 次，如 repeat(5,3) 得到 5,5,5

##### 函数循环器

- chain(p,q,...) 将 p,q,... 等输入都分解，如 chain('abc','efg') 得到 a,b,c,e,f,g
- compress(p,q) 根据 q 每一个值的真假情况，分解 p 的每一个值，如 compress('abcd',[1,0,1,1]) 得到 a,c,d
- dropwhile(fun,q) 根据 函数 func 的返回值真假，一旦函数返回 假，则开始收集剩下的 q，如 dropwhile(lambda x:x>2 ,[8,5,1,3,8]) 得到 1,3,8
- takewhile(fun,q) 根据 函数 func 的返回值真假，一旦函数返回 假，则放弃收集剩下的 q，如 takewhile(lambda x:x>2 ,[8,5,1,3,8]) 得到 8,5
- groupby(p[,func]) 根据 函数 func 的返回值，划分 p 为几个集合 ，两个返回值，第一个返回值是这个函数的返回值，第二个返回值是按照 函数划分的循环对象集合。<br>
	```
    # print nums

    import itertools

    def height_class(h):
        if h > 180:
            return "tall"
        elif h < 160:
            return "short"
        else:
            return "middle"

    friends = [191, 158, 159, 187, 165, 170, 177, 181, 182, 190]

    for m, n in itertools.groupby(friends, key = height_class):
        print m,
        print list(n)
	```
- ifilter(func,q) 与 filter 类似，也是一个过滤函数，返回 func(q[n]) 为真的 q[n] 如 ifilter(lambda x: x > 5, [8, 2, 3, 5, 6, 7]) ，得到 8,6,7
- ifilterfalse(func,q) 与 ifilter 类似，不过返回 func(q[n]) 为假的 q[n] ，如 ifilter(lambda x: x > 5, [8, 2, 3, 5, 6, 7]) 得到 2,3
- islice(seq, [start,] stop [, step]) 类似于 slice 函数，即接片操作，返回 seq[start:stop:step] ，如 islice('abcdefg',2,8,2) ，得到 c,e,g
- imap(func, p, q, ...) 类似于 map 函数，返回 func(p0,q0,...),func(p1,q1,...),... 如 imap(lambda x,y:x+y,[1,2,3,4],[7,8,9,0]) ，得到 8,10,12,4
- starmap(func,q) 类似与 imap 函数，返回 func(q[0]),func(q[1]),... 如 starmap(lambda x,y:x+y,zip([1,2,3,4],[7,8,9,0])) 得到 8,10,12,4
- tee(p,n=1) 由 p 生成 n 个序列，返回这 n 个序列的数组，n 个序列值相同，地址不同,就是将 p 重复输出 n 遍，得到n个迭代器。
- izip(p,q,...) 类似于 zip ，返回 (p0,q0,...),(p1,q1,...),... 如 izip([1,2,3],[4,5,6],[7,8,9]) 得到 (1,4,7),(2,5,8),(3,6,9)
- izip_longest() 类似与 izip ，应该是可以使用数据比 izip 更大一点的吧。

##### 组合工具函数

- product(p, q, ... [,repeat=1]) 取循环集合的笛卡尔积 如 product([1,2,3,4],['a','b','c']) 得到 (1,'a'),(1,'b'),(1,'c'),(2,'a'),(2,'b'),(2,'c')...(4,'b'),(4,'c')
- permutations(q[,r=1]) q 做 r 位的全排列 如 permutations('abcde',3) 得到 ('a', 'b', 'c'),('a', 'b', 'd')...('c','d','e') |共 60 组
- combinations(q,r=1) q 做 r 位的全组合 如 combinations('abcde',3) 得到 ('a', 'b', 'c'),('a', 'b', 'd')...('c','d','e') |共 10 组
- combinations_with_replacement(p,r) 与 combinations 类似 ，但是允许元素重复出现，如 combinations_with_replacement('abcde',3) 得到 ('a', 'a', 'a'),('a', 'a', 'b'),...('e','e','e') | 共 125 组


