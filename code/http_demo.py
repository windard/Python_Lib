# -*- coding: utf-8 -*-

import httplib

connection = httplib.HTTPConnection("httpbin.org")
# 打开日志
connection.set_debuglevel(1)

# GET 请求
connection.request("GET", "/get?name=windard")
response = connection.getresponse()
print "HTTP GET:", response.read()

# POST 请求
connection.request("POST", "/post", '{"haha":"lala"}', {
    "From": "China",
    "To": "USA",
    "Content-Type": "application/json",
})

response = connection.getresponse()
print "HTTP Status Code:", response.status
print "HTTP Version:", response.version
print "HTTP Reason:", response.reason
print "HTTP headers:"
print response.getheaders()

print "HTTP Connection:", response.getheader("Connection")
print "HTTP msg:", response.msg

print "HTTP Body:", response.read()

# 关闭连接
connection.close()
