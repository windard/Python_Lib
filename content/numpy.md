## numpy

numpy 是一个科学计算的库，可以用当做数组使用，提供了矩阵计算的功能，有很多强大的函数。

## numpy 的数组

### 创建数组

用 numpy 创建数组和平常创建数组基本一样，还有创建多维数组，创建元祖，和查看数据类型，只不过数组的元素都必须是数字。

```
>>> import numpy as np
>>> print np.version.version
1.6.1
>>> a = np.array([1,2,3,4,5])
>>> a
array([1, 2, 3, 4, 5])
>>> type(a)
<type 'numpy.ndarray'>
>>> a.dtype
dtype('int32')
>>>
>>> b = np.array(['a','b',3,a])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: cannot set an array element with a sequence
>>> b = np.array((5,6,7,8,2))
>>> b
array([5, 6, 7, 8, 2])
>>> c = np.array([[1,2,3],[4,5,6],[7,8,9]])
>>> len(c)
3
>>> c
array([[1, 2, 3],
       [4, 5, 6],
       [7, 8, 9]])
```

数组的大小可以通过 len 函数或者是其 shape 属性获得，也可以通过其 shape 属性修改。

```
>>> a = np.array([1,2,3,4,5])
>>> a
array([1, 2, 3, 4, 5])
>>> c = np.array([[1,2,3],[4,5,6],[7,8,9]])
>>> c
array([[1, 2, 3],
       [4, 5, 6],
       [7, 8, 9]])
>>> len(a)
5
>>> a.shape
(5,)
>>> c.shape
(3, 3)
>>> c = np.array([[1,2,3,4],[4,5,6,7],[8,9,10,11]])
>>> c
array([[ 1,  2,  3,  4],
       [ 4,  5,  6,  7],
       [ 8,  9, 10, 11]])
>>> c.shape
(3, 4)
>>> c.shape = 4,3
>>> c
array([[ 1,  2,  3],
       [ 4,  4,  5],
       [ 6,  7,  8],
       [ 9, 10, 11]])
>>> c.shape = 2,-1
>>> c
array([[ 1,  2,  3,  4,  4,  5],
       [ 6,  7,  8,  9, 10, 11]])
```

可以通过 reshape 方法改变数组的尺寸，得到一个新的数组，原数组不变，而且两个数组共享数据存储空间。

```
>>> a = np.array([1,2,3,4])
>>> a
array([1, 2, 3, 4])
>>> b = a.reshape((2,2))
>>> b
array([[1, 2],
       [3, 4]])
>>> a[0]=10
>>> a
array([10,  2,  3,  4])
>>> b
array([[10,  2],
       [ 3,  4]])
```

可以通过 dtype 属性获得数组里元素的类型，也可以通过 dtype 属性来设定元素类型。

