## pycurl

功能同 Linux 下的 `curl` 命令，就是一个用于网络通信的 Python 库，因为它是用 C 语言编写的，要比 urllib 快一些，而且它不仅仅支持 'http', 'https' ,还支持 'dict', 'file', 'ftp', 'ftps', 'gopher', 'imap', 'imaps', 'ldap', 'ldaps', 'pop3', 'pop3s', 'rtmp', 'rtsp', 'smtp', 'smtps', 'telnet', 'tftp' 等一系列的网络协议。

```bash
>>> import pycurl
>>> pycurl.version
'PycURL/7.19.3 libcurl/7.35.0 GnuTLS/2.12.23 zlib/1.2.8 libidn/1.28 librtmp/2.3'
>>> pycurl.version_info()
(3, '7.35.0', 467712, 'i686-pc-linux-gnu', 50877, 'GnuTLS/2.12.23', 0, '1.2.8', ('dict', 'file', 'ftp', 'ftps', 'gopher', 'http', 'https', 'imap', 'imaps', 'ldap', 'ldaps', 'pop3', 'pop3s', 'rtmp', 'rtsp', 'smtp', 'smtps', 'telnet', 'tftp'), None, 0, '1.28')
>>> pycurl.version_info()[8]
('dict', 'file', 'ftp', 'ftps', 'gopher', 'http', 'https', 'imap', 'imaps', 'ldap', 'ldaps', 'pop3', 'pop3s', 'rtmp', 'rtsp', 'smtp', 'smtps', 'telnet', 'tftp')

```

#### 初级应用

HTTP 请求中的一切参数都是可以设置的，为你私人订制。

```python
# coding=utf-8

import pycurl
import urllib

c = pycurl.Curl()

# 设置要访问的网址
url = "http://www.windard.com"
c.setopt(pycurl.URL, url)

# 设置请求方式
c.setopt(pycurl.CUSTOMREQUEST,"GET")

# 最大重定向次数,可以预防重定向陷阱
c.setopt(pycurl.MAXREDIRS, 5)

# 连接超时设置
c.setopt(pycurl.CONNECTTIMEOUT, 60)

# 下载超时设置
c.setopt(pycurl.TIMEOUT, 300)

# 可以将请求头一起设置
c.setopt(c.HTTPHEADER, ["Accept : text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","X-Requested-With:XMLHttpRequest","Connection : keep-alive","Accept-Language:zh-CN,zh;q=0.8"])

# 也可以单独设置
c.setopt(c.REFERER, url)
c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36")
c.setopt(pycurl.COOKIE, "session:Cs1LRQ.u4SQWcN5n69FmO6jgKJzEgQq3tc")

# POST 请求参数
# post_data_dic = {"name":"windard"}
# c.setopt(c.POSTFIELDS, urllib.urlencode(post_data_dic))

# POST 上传文件
#post_file = "/home/ubuntu/avatar.jpg"
# c.setopt(c.HTTPPOST, [("textname", (c.FORM_FILE, post_file))])

# 设置代理
# c.setopt(pycurl.PROXY, 'http://11.11.11.11:8080')
# c.setopt(pycurl.PROXYUSERPWD, 'aaa:aaa')

# 执行
c.perform()

print "HTTP-code:", c.getinfo(c.HTTP_CODE) #打印出 200(HTTP状态码)
print "Total-time:", c.getinfo(c.TOTAL_TIME)
print "Download speed: %.2f bytes/second" % c.getinfo(c.SPEED_DOWNLOAD)
print "Document size: %d bytes" % c.getinfo(c.SIZE_DOWNLOAD)
print "Effective URL:", c.getinfo(c.EFFECTIVE_URL)
print "Content-type:", c.getinfo(c.CONTENT_TYPE)
print "Namelookup-time:", c.getinfo(c.NAMELOOKUP_TIME)
print "Redirect-time:", c.getinfo(c.REDIRECT_TIME)
print "Redirect-count:", c.getinfo(c.REDIRECT_COUNT)

c.close()

```

``` bash
<html>XXX<body>XXX</body></html>
HTTP-code: 200
Total-time: 0.733758
Download speed: 139990.00 bytes/second
Document size: 102719 bytes
Effective URL: https://www.baidu.com/
Content-type: text/html; charset=utf-8
Namelookup-time: 0.012367
Redirect-time: 0.126576
Redirect-count: 1

```

跟随了百度的 HTTPS 跳转并找到了真实的网址。

#### 控制输入输出

在上面的例子中，请求得到的结果直接就输出到了屏幕上，我们可以控制请求得到的结果到内存中或者是文件中。

```
# coding=utf-8

import urllib
import pycurl
import StringIO

c = pycurl.Curl()

# 设置要访问的网址
url = "http://www.baidu.com"
c.setopt(pycurl.URL, url)

# 设置请求方式
c.setopt(pycurl.CUSTOMREQUEST,"GET")

# 跟随跳转
c.setopt(pycurl.FOLLOWLOCATION, True)

# 最大重定向次数,可以预防重定向陷阱
c.setopt(pycurl.MAXREDIRS, 5)

# 连接超时设置
c.setopt(pycurl.CONNECTTIMEOUT, 60)

# 下载超时设置
c.setopt(pycurl.TIMEOUT, 300)

# 可以将请求头一起设置
c.setopt(c.HTTPHEADER, ["Accept : text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","X-Requested-With:XMLHttpRequest","Connection : keep-alive","Accept-Language:zh-CN,zh;q=0.8"])

# 也可以单独设置
c.setopt(c.REFERER, url)
c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36")
c.setopt(pycurl.COOKIE, "session:Cs1LRQ.u4SQWcN5n69FmO6jgKJzEgQq3tc")

# # 写入到内存中
# b = StringIO.StringIO()
# c.setopt(pycurl.WRITEFUNCTION, b.write)

# # 执行
# c.perform()

# html = b.getvalue()
# print(html)

# b.close()
# c.close()

# # 写到文件中
# with open('out.html', 'wb') as f:
#     c.setopt(c.WRITEDATA, f)
#     c.perform()
#     c.close()

# 写入到函数中

body = []
header = {}
def write_function(line):
    body.append(line)

def header_function(line):
    if ':' not in line:
        return
    name, value = line.split(':')[:2]
    header[name.strip()] = value.strip()

c.setopt(c.WRITEFUNCTION, write_function)
c.setopt(c.HEADERFUNCTION, header_function)

c.perform()
c.close()

```

在访问 HTTPS 网站时可以会遇到证书错误 `pycurl.error: (60, 'SSL certificate problem: unable to get local issuer certificate')`

可以用 certifi 来定位证书的位置

```
import pycurl
import certifi

curl = pycurl.Curl()
curl.setopt(pycurl.CAINFO, certifi.where())
curl.setopt(pycurl.URL, 'https://www.quora.com')
curl.perform()
``` 