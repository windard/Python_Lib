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
