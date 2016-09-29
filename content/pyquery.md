## pyquery

基于 python 和 jquery 语法操作 XML 的网络编程库。类似于 urllib 与 BeautifulSoup 的结合体。为什么不提 requests ？这个库可能更适合对页面内容的 DOM 元素进行操作,而不是做网络请求。

#### 初始化

PyQuery 提供了四种接口来加载内容。

1. 直接字符串

```
from pyquery import PyQuery as pq
doc = pq("<html></html>")
```

2. lxml.etree

```
from pyquery import PyQuery as pq
from lxml import etree
doc = pq(etree.fromstring("<html></html>"))
```

3. 直接传 URL

```
from pyquery import PyQuery as pq
doc = pq('http://www.baidu.com')
```

4. 传入文件

```
from pyquery import PyQuery as pq
doc = pq(filename='hello.html')
```

#### 简单使用

```
from pyquery import PyQuery as pq
print pq('http://cuiqingcai.com/', headers={'user-agent': 'pyquery'})
print pq('http://httpbin.org/post', {'foo': 'bar'}, method='post', verify=True)
```


#### 参考链接

[pyquery: 基于python和jquery语法操作XML](http://www.geoinformatics.cn/lab/pyquery/)
[Python爬虫利器六之PyQuery的用法](http://cuiqingcai.com/2636.html)
[pyquery: a jquery-like library for python](https://pythonhosted.org/pyquery/)
