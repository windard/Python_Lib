## urlparse

### 简单使用

URL 解析处理函数库，有很多关于 URL 常用的功能。

- `urlparse.urlparse(url, scheme='', allow_fragments=True)` 将 URL 拆分成六元组(<scheme>://<netloc>/<path>;<params>?<query>#<fragment>)。
- `urlparse.urlunparse(data)` 与上面的过程相反，将 六元组 合并成 URL
- `urlparse.urlsplit(url, scheme='', allow_fragments=True)` 将 URL 切割为六元组，与 `urlparse.urlparse` 功能基本一致
- `urlparse.parse_qs(qs, keep_blank_values=0, strict_parsing=0)` 将 GET 请求参数单独切割，生成字典
- `urlparse.parse_qsl(qs, keep_blank_values=0, strict_parsing=0)` 将 GET 请求参数单独切割，生成元组
- `urlparse.urljoin(base, url, allow_fragments=True)` 将两个 URL 合并。

```
>>> import urlparse
>>> url="https://windard.com/2017/03/12/simple?name=windard&year=21#last"
>>> urlparse.urlparse(url)
ParseResult(scheme='https', netloc='windard.com', path='/2017/03/12/simple', params='', query='name=windard&year=21', fragment='last')
>>> urlparse.urlparse(url).scheme
'https'
>>> urlparse.urlparse(url).netloc
'windard.com'
>>> urlparse.urlsplit(url)
SplitResult(scheme='https', netloc='windard.com', path='/2017/03/12/simple', query='name=windard&year=21', fragment='last')
>>> urlparse.urlsplit(url).path
'/2017/03/12/simple'
>>> urlparse.urlsplit(url).query
'name=windard&year=21'
>>> urlparse.urlunparse((urlparse.urlparse(url).scheme, urlparse.urlparse(url).netloc,'','','',''))
'https://windard.com'
>>> urlparse.urlunparse(('http', urlparse.urlparse(url).netloc,'','','',''))
'http://windard.com'
>>> urlparse.parse_qs(url)
{'https://windard.com/2017/03/12/simple?name': ['windard'], 'year': ['21#last']}
>>> urlparse.parse_qs(url, strict_parsing=1)
{'https://windard.com/2017/03/12/simple?name': ['windard'], 'year': ['21#last']}
>>> urlparse.parse_qsl(url)
[('https://windard.com/2017/03/12/simple?name', 'windard'), ('year', '21#last')]
>>> urlparse.parse_qs('https://baidu.com?q=search&p=windard')
{'p': ['windard'], 'https://baidu.com?q': ['search']}
>>> urlparse.parse_qs('https://baidu.com?q=search&p=windard')['p']
['windard']
>>> urlparse.urljoin(url, '/other/path')
'https://windard.com/other/path'
>>> urlparse.urljoin(url, 'http://baidu.com/simple')
'http://baidu.com/simple'
>>> urlparse.urljoin(url, '../../baidu.com/simple')
'https://windard.com/2017/baidu.com/simple'
>>> urlparse.urljoin(url, '../../../../baidu.com/simple')
'https://windard.com/../baidu.com/simple'
```

可以看到大部分都是和想象中的一样，但是有两个问题
- `urlparse.parse_qs` 对 GET 参数的解析不完全，对于第一个解析参数不能正确识别
- `urlparse.urljoin` 在第二个 URL 中含有大量 `../../` 时不能解析正确。

对于第一个问题，下面的函数可以解决

```
# coding=utf-8

def parse_qs(url):
    result = {}
    query = url.partition('?')[2].rpartition('#')[0] if url.find('#') > 0 else url.partition('?')[2]
    for item in query.split('&'):
        key, value = item.split('=')
        result[key] = value
    return result

if __name__ == '__main__':
    url = "https://windard.com/2017/03/12/simple?name=windard&year=21#last"
    print parse_qs(url)
    print parse_qs(url)['name']
    print parse_qs(url)['year']

    url = "https://baidu.com?q=search&p=windard"
    print parse_qs(url)
    print parse_qs(url)['q']
    print parse_qs(url)['p']

```

输出

```
{'name': 'windard', 'year': '21'}
windard
21
{'q': 'search', 'p': 'windard'}
search
windard
```

对于第二个问题，下面的函数可以解决

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

输出

```
http://www.baidu.com/abc.html
http://www.baidu.com/abc.html
http://www.baidu.com/abc.html
http://www.baidu.com/abc.html?key=value&m=x
```


### 其他使用

- urllib.urlencode  <-> urlparse.parse_qsl
- urllib.quote      <-> urllib.unquote
- urlparse.urlparse <-> urlparse.urlunparse