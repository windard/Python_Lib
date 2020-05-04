# -*- coding: utf-8 -*-

import urllib
import urllib2


def urllib_proxy():
    resp = urllib.urlopen("http://httpbin.org/ip", proxies={
        "http": "http://117.69.152.162:8691"
    })
    print resp.read()


def urllib2_proxy():
    proxy_handler = urllib2.ProxyHandler({
        "http": "http://117.69.152.162:8691"
    })
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)

    resp = urllib2.urlopen("http://httpbin.org/ip")
    print resp.read()


if __name__ == '__main__':
    urllib_proxy()
    urllib2_proxy()
