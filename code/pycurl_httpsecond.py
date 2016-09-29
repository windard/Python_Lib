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
