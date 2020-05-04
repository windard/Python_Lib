# -*- coding: utf-8 -*-

import urllib

data = {
    "name": "windard",
    "country": "china",
}

data_string = urllib.urlencode(data)

# 发起请求
resp = urllib.urlopen("http://httpbin.org/post", data_string)

# 返回是一个类 file 对象，可以通过 read() 读取
print resp.read()
