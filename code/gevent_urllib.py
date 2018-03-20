# coding=utf-8

import time
from gevent import monkey
import gevent
import urllib2


monkey.patch_all()


def spend_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        rv = func(*args, **kwargs)
        end_time = time.time()
        print end_time - start_time
        return rv
    return wrapper


def request(url):
    print('GET: %s' % url)
    resp = urllib2.urlopen(url)
    data = resp.read()
    print('%d bytes received from %s.' % (len(data), url))


@spend_time
def in_order(urls):
    for url in urls:
        request(url)


@spend_time
def in_concur(urls):
    spawns = []
    for url in urls:
        spawns.append(gevent.spawn(request, url))

    gevent.joinall(spawns)


def main():
    urls = ['https://baidu.com', 'https://zhihu.com', 'https://ele.me']
    in_order(urls)
    in_concur(urls)


if __name__ == '__main__':
    main()
