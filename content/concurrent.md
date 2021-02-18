## concurrent

python 中的异步库，集成 threading 和 multiprocessing 两个库。

可以使用 `ThreadPoolExecutor` 和 `ProcessPoolExecutor` 来做线程和进程

### 简单使用

这个库使用很简单，常见方法也即那么几种
> [concurrent.futures --- 启动并行任务](https://docs.python.org/zh-cn/3/library/concurrent.futures.html)

- concurrent.futures.Executor|ThreadPoolExecutor|ProcessPoolExecutor
    - submit
    - map
    - shutdown
- concurrent.futures.Future
    - cancel
    - cancel
    - cancel
    - done
    - cancel
    - exception
    - add_done_callback
- concurrent.futures.wait
- concurrent.futures.as_completed

```python
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

### 动态添加任务

```python
# -*- coding: utf-8 -*-
import time
import random
import traceback

from concurrent import futures
from concurrent.futures import ThreadPoolExecutor

result = []


def handle(num, pool):
    try:
        print("thread for:%d" % num)
        sleep_time = random.random()
        time.sleep(sleep_time)
        if sleep_time < 0.95:
            print("thread pool add one")
            print("before pool size:%d" % pool._work_queue.qsize())
            pool.submit(handle, num*10, pool)
            # result.append(pool.submit(handle, 111, pool))
            print("after pool size:%d" % pool._work_queue.qsize())
    except Exception as e:
        # 问题在这里:
        # py2: cannot schedule new futures after shutdown
        # py3: cannot schedule new futures after interpreter shutdown
        print(repr(e))
        traceback.print_stack()


if __name__ == '__main__':
    # 使用 map 的时候需要注意，其实 pool 会自动帮你把参数 zip 一下，先合并再分别映射
    # 其实最后不用调用 shutdown 也会自动等待所有任务结束，然后主进程结束
    thread_pool = ThreadPoolExecutor(30)
    # map_result = thread_pool.map(handle, range(2), [thread_pool] * 2)
    # result.extend(list(map_result))
    # 实际上，使用 submit 多个参数的时候也需要注意，参数直接摆开，和 threading 不一样
    for i in range(4):
        result.append(thread_pool.submit(handle, i, thread_pool))
    print("start threading")
    # 在没有 shutdown 之后为什么还会自动结束呢？谁在
    # thread_pool.shutdown()
    while result:
        print("before result length:%d" % len(result))
        for f in futures.as_completed(result):
            result.remove(f)
        # 此处还是有风险，如果这里结束了，全都结束了之后，还是会自动调用 shutdown
        # 其实还有待提交的请求，这样就尴尬了。
        # 但是加等待时间也不能够
        if len(result) == 0:
            time.sleep(2)
        print("after result length:%d" % len(result))
        # 还是用 lock 锁定一个计数器比较现实，计数器归零再结束。

    # futures.wait(result)
    # thread_pool.shutdown()
    # 不需要 as_completed 也不需要手动 wait，实际上在 shutdown 的时候其实就是会等待结束的
    # 如果使用上下文管理器的话会自动 shutdown
    # 问题是在子线程中不能再往线程中加任务了，有点问题
    # with ThreadPoolExecutor(30) as thread_pool:
    #     result = thread_pool.map(handle, range(2), [thread_pool] * 2)
    #     print("start threading")
    #     thread_pool.submit(handle, 111, thread_pool)

```

参考链接

[使用Python进行并发编程-PoolExecutor篇](http://www.dongwm.com/archives/%E4%BD%BF%E7%94%A8Python%E8%BF%9B%E8%A1%8C%E5%B9%B6%E5%8F%91%E7%BC%96%E7%A8%8B-PoolExecutor%E7%AF%87/)  
[使用Python的 concurrent.futures 模块](https://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/chapter4/02_Using_the_concurrent.futures_Python_modules.html)  
[python并发库：concurrent.futures的使用](https://blog.csdn.net/drdairen/article/details/69487643)   
[python并发 1：使用 futures 处理并发](https://segmentfault.com/a/1190000009819359)    
