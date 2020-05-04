# -*- coding: utf-8 -*-

import urllib

# 发起请求
resp = urllib.urlopen("http://httpbin.org/get")

# 返回是一个类 file 对象，可以通过 read() 读取
print resp.read()

print "HTTP Status Code:", resp.getcode()
print "HTTP Request Url:", resp.geturl()
print "HTTP Response Headers:"
print resp.info()
print "HTT Content-Length:", resp.info().get("Content-Length")
