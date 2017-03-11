## urlparse

URL 解析处理函数库，有很多使用的功能。

urljoin(base, url, allow_fragments=True)

urldefrag(url)

urlparse(url, scheme='', allow_fragments=True)

urlsplit(url, scheme='', allow_fragments=True)

parse_qs(qs, keep_blank_values=0, strict_parsing=0) # 连 GET 请求参数一起解析

```
# coding=utf-8

from urlparse import urljoin
from urlparse import urlparse
from urlparse import urlunparse
from posixpath import normpath
 
def myjoin(base, url):
    url1 = urljoin(base, url)
    arr = urlparse(url1)
    path = normpath(arr[2])
    return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))
 
if __name__ == "__main__":
    print myjoin("http://www.baidu.com", "abc.html")
    print myjoin("http://www.baidu.com", "/../../abc.html")
    print myjoin("http://www.baidu.com/xxx", "./../../abc.html")
    print myjoin("http://www.baidu.com", "abc.html?key=value&m=x")
```