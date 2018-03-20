# coding=utf-8

from functools import wraps
import time
import urllib


def web_lookup(url, saved={}):
    if url in saved:
        return saved[url]
    page = urllib.urlopen(url).read()
    saved[url] = page
    return page


def cache(func):
    saved = {}

    @wraps(func)
    def new_func(*args):
        if args in saved:
            return saved[args]
        result = func(*args)
        saved[args] = result
        return result
    return new_func


@cache
def web_lookup(url):
    return urllib.urlopen(url).read()


@cache
def test_cache(n):
    return time.time()

# print test_cache(1)
# time.sleep(3)
# print test_cache(1)
# time.sleep(3)
# print test_cache(1)


def time_cache(n, saved={}):
    if n in saved:
        return saved[n]
    result = time.time()
    saved[n] = result
    return result

print time_cache(1)
time.sleep(2)
print time_cache(1)
time.sleep(2)
print time_cache(1)
