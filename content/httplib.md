## httplib

不推荐用 urllib 和 urllib2 ，最好用 requests，否则就用 httplib, httplib 是 urllib 和 urllib2 的底层库，但是使用起来和 requests 一样简单。

urllib 使用的是 httplib.HTTP, urllib2 使用的是 httplib.HTTPConnection 

根据历史的发展，我们知道用 HTTPConnection 应该是对的。然后阅读源码，证明我们的结论，HTTP 只是为了兼容历史版本，而且也改成了使用 HTTPConnection 的方式。

httplib 在 python3 中被换了个位置，变成了 http.client ，所有的引入方式从 `from httplib import **` 变成 `from http.client import **` 即可

为了让 python2 与 python3 兼容，在 python2 中也可以用 `http.client` 引入 httplib

### HTTP 

httplib 作为一个基础库，首先定义了一些 HTTP 的常用枚举，包括 HTTP 的状态码和对应的解释说明。

```
# status codes
# informational
CONTINUE = 100
SWITCHING_PROTOCOLS = 101
PROCESSING = 102

# successful
OK = 200
CREATED = 201
ACCEPTED = 202
NON_AUTHORITATIVE_INFORMATION = 203
NO_CONTENT = 204
RESET_CONTENT = 205
PARTIAL_CONTENT = 206
MULTI_STATUS = 207
IM_USED = 226

# redirection
MULTIPLE_CHOICES = 300
MOVED_PERMANENTLY = 301
FOUND = 302
SEE_OTHER = 303
NOT_MODIFIED = 304
USE_PROXY = 305
TEMPORARY_REDIRECT = 307

# client error
BAD_REQUEST = 400
UNAUTHORIZED = 401
PAYMENT_REQUIRED = 402
FORBIDDEN = 403
NOT_FOUND = 404
METHOD_NOT_ALLOWED = 405
NOT_ACCEPTABLE = 406
PROXY_AUTHENTICATION_REQUIRED = 407
REQUEST_TIMEOUT = 408
CONFLICT = 409
GONE = 410
LENGTH_REQUIRED = 411
PRECONDITION_FAILED = 412
REQUEST_ENTITY_TOO_LARGE = 413
REQUEST_URI_TOO_LONG = 414
UNSUPPORTED_MEDIA_TYPE = 415
REQUESTED_RANGE_NOT_SATISFIABLE = 416
EXPECTATION_FAILED = 417
UNPROCESSABLE_ENTITY = 422
LOCKED = 423
FAILED_DEPENDENCY = 424
UPGRADE_REQUIRED = 426

# server error
INTERNAL_SERVER_ERROR = 500
NOT_IMPLEMENTED = 501
BAD_GATEWAY = 502
SERVICE_UNAVAILABLE = 503
GATEWAY_TIMEOUT = 504
HTTP_VERSION_NOT_SUPPORTED = 505
INSUFFICIENT_STORAGE = 507
NOT_EXTENDED = 510

# Mapping status codes to official W3C names
responses = {
    100: 'Continue',
    101: 'Switching Protocols',

    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    203: 'Non-Authoritative Information',
    204: 'No Content',
    205: 'Reset Content',
    206: 'Partial Content',

    300: 'Multiple Choices',
    301: 'Moved Permanently',
    302: 'Found',
    303: 'See Other',
    304: 'Not Modified',
    305: 'Use Proxy',
    306: '(Unused)',
    307: 'Temporary Redirect',

    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    406: 'Not Acceptable',
    407: 'Proxy Authentication Required',
    408: 'Request Timeout',
    409: 'Conflict',
    410: 'Gone',
    411: 'Length Required',
    412: 'Precondition Failed',
    413: 'Request Entity Too Large',
    414: 'Request-URI Too Long',
    415: 'Unsupported Media Type',
    416: 'Requested Range Not Satisfiable',
    417: 'Expectation Failed',

    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
    505: 'HTTP Version Not Supported',
}
```

### 请求

httplib 中最重要的两个类 `HTTPConnection` 和 `HTTPSConnection` 分别对应 HTTP 请求和 HTTPS 请求。

可以先看下请求过程，在源代码注释中为我们画了这样一幅图。

```
    (null)
      |
      | HTTPConnection()
      v
    Idle
      |
      | putrequest()
      v
    Request-started
      |
      | ( putheader() )*  endheaders()
      v
    Request-sent
      |
      | response = getresponse()
      v
    Unread-response   [Response-headers-read]
      |\____________________
      |                     |
      | response.read()     | putrequest()
      v                     v
    Idle                  Req-started-unread-response
                     ______/|
                   /        |
   response.read() |        | ( putheader() )*  endheaders()
                   v        v
       Request-started    Req-sent-unread-response
                            |
                            | response.read()
                            v
                          Request-sent
```

发起 HTTP 请求

```
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
```

使用 HTTPConnection 可以自己手动设置发送请求方式，请求头，请求参数，请求体，比较自由。

