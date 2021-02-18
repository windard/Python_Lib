## funcy

一个非常简单实用的库，有很多的工具函数，提供了一些函数式编程的增强功能。
> 现在还能见到同时支持 Python2 和 Python3 的库，也是非常的良心了。 👍   
> 而且对于列表的处理，在 Python2 里返回 list，在 Python3 里返回迭代器，还同时在 Python2 中支持迭代器形式的返回，在 Python3 中支持 list 形式的返回。细节满分，i了i了。 ❤️

## 安装

```
pip install funcy
```

## 简单应用

### 字符串和列表

#### flatten

展开列表，这是一个很常见的场景，把列表中的列表中的列表都展开为单层

```python
# -*- coding: utf-8 -*-

import funcy as fc
# only support in python2
from compiler.ast import flatten as ast_flatten


def flatten(elements):
    result = []
    for item in elements:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def old_flatten(elements):
    return [_ for item in elements for _ in old_flatten(item)] if isinstance(elements, list) else [elements]
    # result = []
    # for item in elements:
    #     if isinstance(item, list):
    #         item = old_flatten(item)
    #     else:
    #         item = [item]
    #     result.extend(item)
    # return result


if __name__ == '__main__':
    a = [1, 2, [3, 4, [5, 6], [7, 8]], [9, 10]]
    print(fc.flatten(a))
    print(ast_flatten(a))
    print(flatten(a))

```

#### distinct

像一些简单的去重，分组就不说了，复杂的可以查文档

```python
# -*- coding: utf-8 -*-
import funcy as fc

if __name__ == '__main__':
    a = [1,3,4,5,2,5,1,5,2,5,1]
    print(fc.distinct(a))
    print(set(a))

    # 按个数分组,舍弃多余的元素
    print(fc.partition(2, range(10)))
    print(fc.partition(3, range(10)))
    # 按个数分组,多余的元素单列
    print(fc.chunks(2, range(10)))
    print(fc.chunks(3, range(10)))

    # 此处不能用 lstrip 或者 rstrip, 因为会将输入字符串当成字符数组
    print("open_api_enforce_interface".lstrip("open_api"))
    print("open_api_enforce_interface".rstrip("_interface"))
    print(fc.cut_prefix("open_api_test_interface", "open_api"))
    print(fc.cut_suffix("open_api_test_interface", "interface"))

``` 

输出

```
[1, 3, 4, 5, 2]
set([1, 2, 3, 4, 5])
[[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]
[[0, 1, 2], [3, 4, 5], [6, 7, 8]]
[[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]
[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
force_interface
open_api_enfo
_test_interface
open_api_test_
```

### 装饰器

#### 重试

错误重试的装饰器有很多，也可以自己简单实现一下，在 funcy 提供的重试装饰器中，还可以指定异常类型和重试间隔时间

只是有一个问题是没有打印错误日志，所有的错误请求都被吞掉了。

```python
# -*- coding: utf-8 -*-
import time
import funcy as fc

from functools import wraps

# def retry(times=3):
#     def inner(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             for i in range(times):
#                 try:
#                     return func(*args, **kwargs)
#                 except Exception as e:
#                     if i == times-1:
#                         raise e
#                     print("occur error:%r" % e)
#
#         return wrapper
#     return inner

# def retry(times=3):
#     def inner(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             try:
#                 return func(*args, **kwargs)
#             except Exception as e:
#                 if times <= 1:
#                     raise e
#                 print("occur error:%r" % e)
#                 return retry(times-1)(func)(*args, **kwargs)
#
#         return wrapper
#
#     return inner


def retry(times=3):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            count = 0
            while count < times:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print("occur error:%r" % e)
                    count += 1
            raise
        return wrapper

    return inner


@fc.retry(5)
# @retry(3)
def raise_exception():
    time.sleep(1)
    return 1 / 0


if __name__ == '__main__':
    print(raise_exception())

```

#### 缓存

本地缓存，或者说内存缓存，将函数调用结果本地缓存起来加速计算过程，funcy 提供的装饰器还把缓存数据挂在函数上了

只有一个问题就是默认的缓存key 太不讲究了,直接是一个 tuple。不过可以传入 key 的生成函数。

```python
# -*- coding: utf-8 -*-
import time
import funcy as fc

from functools import wraps


def cache(func):
    local_cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = "{}:{}".format(";".join(map(str, args)),
                             ";".join(["{}:{}".format(*map(str, item)) for item in sorted(kwargs.items())]))
        if key in local_cache:
            return local_cache[key]
        else:
            value = func(*args, **kwargs)
            local_cache[key] = value
            return value

    return wrapper


# @cache
@fc.memoize
def get_timestamp(x):
    return int(time.time())


if __name__ == '__main__':
    print(get_timestamp(1))
    time.sleep(1)
    print(get_timestamp(1))
    time.sleep(1)
    print(get_timestamp(1))
    time.sleep(2)
    print(get_timestamp(2))
    time.sleep(1)
    print(get_timestamp(2))
    print(get_timestamp.memory)
```

#### once

这个就比较简单了，像 Golang 里的 Once ，就是限制函数只能被调用一次，使用的 threading.Lock 加锁。

```python
# -*- coding: utf-8 -*-
import funcy as fc


@fc.once
def call_once():
    print("only once called")


@fc.once
def call_once_with_args(x):
    print("only once with args called")


if __name__ == '__main__':
    call_once()
    call_once()
    call_once_with_args(1)
    call_once_with_args(2)

```

### 总结

确实有不少好东西可以学习借鉴，可以查看文档或者速查表来找找有没有合适的工具。

突然想起来，还一个单例模式，竟然没有提供，大意了吖。

### 参考链接

[funcy document](https://funcy.readthedocs.io/en/stable/overview.html)  
[给大家推荐一个堪称瑞士军刀的 Python 库](https://mp.weixin.qq.com/s/wIOae8ASUp3_zpBn4kMweg)  
[retry_with_times](https://gist.github.com/windard/0847d44af575cc44be419dbab4602241)   


