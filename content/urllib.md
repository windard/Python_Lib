## urllib

对于这个库，最好的建议就是不要用。用 requests 吧，for human 。


### 使用

开始的开始，只是发送一个简单的请求，返回是一个 IO 对象，也就是可以用 `read`, `readline` 或者 `readlines` 等读取响应内容。

```
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

```

返回对象中除了正常的读取响应内容之外，还有额外的三个方法，分别是
- `getcode` 获取返回状态
- `geturl` 获取请求 URL
- `info` 获取返回响应头

#### GET 参数

主要就是 `urllib.urlencode` 会将参数进行编码，然后需要手动加到请求 URL 中

```
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

```

`urllib.urlencode` 的必填参数需要是一个字典，其中 value 的值有可能是一个列表，那么会根据其第二个参数 `doseq` 来决定其展现形式

例如

```
{"city": ["Beijing", "Shanghai", "Nanjing"]}
```

进行 urlencode 的结果是

```
city=%5B%27Beijing%27%2C+%27Shanghai%27%2C+%27Nanjing%27%5D
```

进行 decode 可以其实是原样输出，然后空格会被转换成 `+`

```
city=['Beijing',+'Shanghai',+'Nanjing']
```

如果 `doseq=1` 的结果会是这样

```
city=Beijing&city=Shanghai&city=Nanjing
```

这也是 URL 里传参数的一种不同的展现形式，但是我还见过其他两种

PHP 中，对于列表的参数需要在字段名中加中括号

```
city[]=["Beijing","Shanghai","Nanjing"]
```

或者将字段的值进行 json 编码

```
city=["Beijing","Shanghai","Nanjing"]
```

#### POST 数据

```
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

```

可以看到基本是和 GET 请求一样的操作，需要先进行 `urlencode` ，然后作为 `urlopen` 的第二个参数传入.

这里就是 urllib 坑的地方了，首先作为 post data，还需要我手动的组装参数。然后也没有传入 GET 还是 POST 请求，而是根据 `urllib` 第二个参数 data 的是否传入来判断。最后，还没有设置 headers 的地方，虽然可以传入 context 中设置，但是也足够复杂。

查看源码可以发现，内部实现逻辑十分的简单粗暴，而且 POST 数据也只能是按照 `x-www-form-urlencode` 格式

```
if data is not None:
    h.putrequest('POST', selector)
    h.putheader('Content-Type', 'application/x-www-form-urlencoded')
    h.putheader('Content-Length', '%d' % len(data))
else:
    h.putrequest('GET', selector)
```

实际上我们知道，POST 请求数据格式有多种，常见的还有两种 `form-data` 和 `json`
- form-data ，一般用来传文件，`Content-Type` 为 `multipart/form-data; boundary=%s` boundary 为分隔符,一般为16位十六进制随机字符
- json, GET 请求或者 POST 请求都可以使用，`Content-Type` 为 `application/json`

通过查看源码，我们也可以发现，urllib 底层实际使用的是 `http` 库，在使用 `urllib.urlopen` 的时候也能够发现警告

```
urllib.urlopen() has been removed in Python 3.0 in favor of urllib2.urlopen()
```

顺便提一嘴，除了 HTTP 协议，urllib 还支持 https,ftp,file,data 等协议，最后的两个是什么呢？
- file 即文件浏览协议，可以通过 `file://filepath` 查看文件内容
- data 即文件内容协议，比如一些网页图片即是通过 base64 编码后用 `data:image/png;base64,xxxx` 表示

### 其他

#### 文件下载

```
# -*- coding: utf-8 -*-

import urllib

filename, headers = urllib.urlretrieve("http://techslides.com/demos/sample-videos/small.mp4")

print "filename: ", filename
print "headers : "
print headers

```

使用 `urllib.urlretrieve` 下载文件，如果没有指定文件名的话，就会放在创建临时文件，放在临时文件夹中

可以通过 `urllib.urlcleanup` 来清理缓存和临时文件

其实完全可以自己实现下载，比如同样功能代码

```
# -*- coding: utf-8 -*-


url = "http://techslides.com/demos/sample-videos/small.mp4"
filename = url.split('/')[-1]

resp = urllib.urlopen(url)
with open(filename, "w") as f:
    chunk = resp.read(1024)
    while chunk:
        f.write(chunk)
        chunk = resp.read(1024)

print "filename: ", filename

```

#### 编码解密

```
# -*- coding: utf-8 -*-

import urllib

params = "https://windard.com"

print urllib.quote(params)
print urllib.quote_plus(params)
print urllib.unquote(urllib.quote(params))
print urllib.unquote_plus(urllib.quote_plus(params))

```

四大金刚
- quote: 编码，主要是将一些 URL 中无法传输的字符转为十六进制，即进行 `'%{:02X}'.format(i)`
- quote_plus: 编码，比 quote 加强一点的是把空格 ` ` 转为加号 `+`
- unquote: quote 解码
- unquote_plus: quote_plus 解码

可以发现，其实 `urllib.urlencode` 就是对参数进行了组装和编码,然后就可以放到 URL 中作为参数传输。

