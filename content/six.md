## six

six = 2 * 3

这是一个用来做 python2 和 python3 兼容的库

主要是内置的一些变量可以用

```
# coding=utf-8

import six

six.print_(six.PY2)
six.print_(six.PY3)

six.print_(six.string_types)


```

python2 和 python3 的结果完全不同

python2

```
True
False
(<type 'basestring'>,)
```

python3

```
False
True
(<class 'str'>,)
```

好吧。

在 1.10.0 的版本里，python2

```
string_types = (str, unicode)
```

在 1.11.0 的版本里,python2

```
string_types = basestring,
```

