# coding=utf-8

import pycurl
import urllib

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
