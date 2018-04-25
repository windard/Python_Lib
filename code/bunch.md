## bunch

将字典转换为类对象使用，可以使用点来取得字典的值

其实自己实现的话

```
# -*- coding: utf-8 -*-


class DotDict(dict):

    def __init__(self):
        super(DotDict, self).__init__()
        self.__dict__ = self


if __name__ == '__main__':

    a = DotDict()
    a['name'] = 'windard'
    a.year = 24
    print a

```

或者这样，这也是 `dotdict` 这个库的全部内容

```
# -*- coding: utf-8 -*-


class DotDict(dict):

    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__
    __delattr__ = dict.__delitem__


if __name__ == '__main__':

    a = DotDict()
    a['name'] = 'windard'
    a.year = 24
    print a
    print a.name

```

而 bunch 的实现是这样的

```
# -*- coding: utf-8 -*-


class DotDict(dict):

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(item)

    def __setattr__(self, key, value):
        try:
            self[key] = value
        except:
            raise AttributeError(key)


    def __delattr__(self, item):
        try:
            del self[item]
        except:
            raise AttributeError(item)


if __name__ == '__main__':

    a = DotDict()
    a['name'] = 'windard'
    a.year = 24
    print a
    print a.name

```

基本上是一个思路，然后再加了一些捕获异常和类型转换，更容易的转换为其他的数据结构。

