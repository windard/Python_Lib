# -*- coding: utf-8 -*-

import urllib


param = {
    "name": "windard",
    "country": "china",
}

query_string = urllib.urlencode(param)

# 发起请求
resp = urllib.urlopen("http://httpbin.org/get"+"?"+query_string)

# 返回是一个类 file 对象，可以通过 read() 读取
print resp.read()
