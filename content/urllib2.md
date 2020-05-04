## urllib2

比 urllib 稍微强那么一点点的库。

### 使用

可以看到基本上使用还是和 urllib 是一样的，向下兼容。返回值里多两个字段 `code` 和 `msg` 分别表示 HTTP 返回状态和状态说明。

```
# -*- coding: utf-8 -*-

import urllib2


# 发起请求
resp = urllib2.urlopen("http://httpbin.org/get")

# 返回是一个类 file 对象，可以通过 read() 读取
print resp.read()

print "HTTP code", resp.code
print "HTTP msg", resp.msg
print "HTTP Status Code:", resp.getcode()
print "HTTP Request Url:", resp.geturl()
print "HTTP Response Headers:"
print resp.info()
print "HTT Content-Length:", resp.info().get("Content-Length")

```

### 实战

urllib 和 urllib2 用起来差不多，深入源码可以发现，其实 urllib 和 urllib2 底层使用的都是 http 库的连接 connection 然后 send 请求。

但是请求中最关键的 `opener` 和 `request` 在 urllib2 中可以被定制，传入自定义实现，而 urllib 中则不行。

#### Headers

所以我们能够在请求 Request 中自定义 headers


不过 HTTP GET 请求和 HTTP POST 请求还是分不清。

```
    def get_method(self):
        if self.has_data():
            return "POST"
        else:
            return "GET"

    def has_data(self):
        return self.data is not None
```

POST 请求

```
# -*- coding: utf-8 -*-

import urllib
import urllib2


headers = {
    "From": "China",
    "Year": "2020",
}

data = {
    "name": "windard",
    "country": "china",
}

request = urllib2.Request("http://httpbin.org/post", headers=headers)
request.add_data(urllib.urlencode(data))
request.add_header("To", "USA")

resp = urllib2.urlopen(request)
print resp.read()

```

POST 数据可以放在 Request 的实例参数中，也可以通过 `add_data` 参数添加，或者在 `urlopen` 参数中添加。

> 在这里需注意，还是需要 `urlencode` 对参数进行编码

headers 可以防止 Request 的实例参数中，也可以通过 `add_header` 参数添加。

#### cookies

当我们需要 cookie 的时候，可以直接在 headers 中写 cookie ，或者使用 CookieJar .

```
# -*- coding: utf-8 -*-

import cookielib
import urllib2


def creat_cookie(name, value, **kwargs):
    result = {
        'version': 0,
        'name': name,
        'value': value,
        'port': None,
        'domain': '',
        'path': '/',
        'secure': False,
        'expires': None,
        'discard': True,
        'comment': None,
        'comment_url': None,
        'rest': {'HttpOnly': None},
        'rfc2109': False,
    }
    result.update(kwargs)
    result['port_specified'] = bool(result['port'])
    result['domain_specified'] = bool(result['domain'])
    result['domain_initial_dot'] = result['domain'].startswith('.')
    result['path_specified'] = bool(result['path'])

    return cookielib.Cookie(**result)


def header():
    cookie_jar = cookielib.CookieJar()
    cookie_handler = urllib2.HTTPCookieProcessor(cookie_jar)
    opener = urllib2.build_opener(cookie_handler)

    request = urllib2.Request("http://httpbin.org/cookies")
    request.add_header("Cookie", "name=windard")

    resp = opener.open(request)
    print resp.read()

    for cookie in cookie_jar:
        print cookie.name, ":", cookie.value


def main():
    cookie_jar = cookielib.CookieJar()
    cookie_handler = urllib2.HTTPCookieProcessor(cookie_jar)
    opener = urllib2.build_opener(cookie_handler)
    cookie_jar.set_cookie(creat_cookie("name", "Windard"))
    cookie_jar.set_cookie(creat_cookie("location", "Shanghai"))

    resp = opener.open("http://httpbin.org/cookies")
    print resp.read()

    for cookie in cookie_jar:
        print cookie.name, ":", cookie.value


if __name__ == '__main__':
    header()

```

#### BasicAuth

使用 HTTP 基本认证，一般常见形式如下

![http_basic_auth_demo](/images/http_basic_auth_demo.png)

虽然在网页上使用的时候只需要输入用户名和密码，但是在实际使用的时候，资源域和资源地址都要输入无误才行，否则就会返回 401 UNAUTHORIZED

```
# -*- coding: utf-8 -*-

import urllib2

# first try
try:
    resp = urllib2.urlopen("http://httpbin.org/basic-auth/admin/password")
    print resp.read()
except Exception as e:
    print "error", e


# with basic auth
basic_auth = urllib2.HTTPBasicAuthHandler()
basic_auth.add_password(
    realm="Fake Realm",  # 资源域空间
    uri="http://httpbin.org/basic-auth/admin/password",  # 资源地址
    user='admin',  # 用户名
    passwd='password'  # 密码
)

opener = urllib2.build_opener(basic_auth)
urllib2.install_opener(opener)


# second try
try:
    resp = urllib2.urlopen("http://httpbin.org/basic-auth/admin/password")
    print resp.read()
except Exception as e:
    print "error", e

```

除了 HTTP Basic Auth 认证方式，还支持 Digest Auth 的方式，使用 `HTTPDigestAuthHandler` 即可。

#### Proxy

配置代理，可惜只有 HTTP 和 HTTPS 代理，并没有 sock5 代理。

```
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

```

urllib 也可以配置代理，其配置在 `urllib.urlopen` 参数中。

### urllib 和 urllib2 异同

相同
1. urllib 和 urllib2 都是用来发送 HTTP 请求，HTTPS，FTP  均可。
2. urllib 和 urllib2 都是根据 data 来区分 GET 和 POST，且没有其他请求方式
3. urllib 和 urllib2 都有`urlopen`, `quote`, `quote_plus` 等方法
4. urllib 和 urllib2 都能配置代理

不同
1. urllib 有 `urlencode`,`urlretrieve` ，而 urllib2 没有
2. urllib2 可以设置 headers ，urllib 不能

