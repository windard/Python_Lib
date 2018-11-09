## concurrent

python 中的异步库，集成 threading 和 multiprocessing 两个库。

可以使用 `ThreadPoolExecutor` 和 `ProcessPoolExecutor` 来做线程和进程


```
# -*- coding: utf-8 -*-

import time
import requests
import functools
from concurrent import futures


def time_count(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print "time", end - start
        return result
    return wrapper


urls = ['https://ele.me',
        'https://baidu.com',
        'https://jd.com',
        'https://v2ex.com',
        'https://windard.com',
        'https://taobao.com',
        'https://zhihu.com',
        'https://vip.com',
        'https://t.tt']


@time_count
def main():
    executor = futures.ThreadPoolExecutor()
    roads = []
    results = []
    for url in urls:
        future = executor.submit(requests.get, url)
        roads.append(future)

    for future in futures.as_completed(roads):
        result = future.result()
        results.append(result.status_code)

    executor.shutdown()
    return results


@time_count
def sync_main():
    with futures.ThreadPoolExecutor() as executor:
        roads = executor.map(requests.get, urls)
        results = [result.status_code for result in roads]
    return results


@time_count
def async_main():
    results = []
    for url in urls:
        results.append(requests.get(url).status_code)
    return results


if __name__ == '__main__':
    print main()
    print async_main()
    print sync_main()

```

参考链接

[使用Python进行并发编程-PoolExecutor篇](http://www.dongwm.com/archives/%E4%BD%BF%E7%94%A8Python%E8%BF%9B%E8%A1%8C%E5%B9%B6%E5%8F%91%E7%BC%96%E7%A8%8B-PoolExecutor%E7%AF%87/)

[使用Python的 concurrent.futures 模块](https://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/chapter4/02_Using_the_concurrent.futures_Python_modules.html)

[python并发库：concurrent.futures的使用](https://blog.csdn.net/drdairen/article/details/69487643)

[python并发 1：使用 futures 处理并发](https://segmentfault.com/a/1190000009819359)
