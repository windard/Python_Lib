## array

一个基础的 Python 内置库，不应该这么晚才发现，看来真的没有将 Python 用到正途上。

array 的功能很简单，很单一，就是创建数组，统一数据类型结构的数组，还能对数组做文件的读写操作，快如闪电。

array 的可以使用的数据类型。

|        Type code  | C Type                |    Minimum size in bytes  |
|------------------ |--------------         |---------------------      |
|        'c'        | character             | 1                         |
|        'b'        | signed integer        | 1                         |
|        'B'        | unsigned integer      | 1                         |
|        'u'        | Unicode character     | 2                         |
|        'h'        | signed integer        | 2                         |
|        'H'        | unsigned integer      | 2                         |
|        'i'        | signed integer        | 2                         |
|        'I'        | unsigned integer      | 2                         |
|        'l'        | signed integer        | 4                         |
|        'L'        | unsigned integer      | 4                         |
|        'f'        | floating point        | 4                         |
|        'd'        | floating point        | 8                         |


```
# coding=utf-8

from array import array
from random import random

floats = array('d', (random() for i in xrange(10**7)))

print floats[-1]

fp = open('floats.bin', 'wb')
floats.tofile(fp)
fp.close()

floats2 = array('d')
fp = open('floats.bin', 'rb')
floats2.fromfile(fp, 10**7)
fp.close()

print floats2[-1]

print floats == floats2

```
