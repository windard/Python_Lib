## CGIHTTPServer

这也是一个 HTTP 服务器，但是比 SimpleHTTPServer 要高级一些，支持 CGI 脚本，也就是说可以用来写后台，接收 POST 请求。

CGI (Common Gateway Interface) 通用网关接口，是服务器与应用脚本之间的一系列接口标准，也就是 PHP 等动态后台脚本语言的基础。

```python
# coding=utf-8
# Written by Vamei
# A messy HTTP server based on TCP socket 

import BaseHTTPServer
import CGIHTTPServer

HOST = ''
PORT = 8001

# Create the server, CGIHTTPRequestHandler is pre-defined handler
server = BaseHTTPServer.HTTPServer((HOST, PORT), CGIHTTPServer.CGIHTTPRequestHandler)
# Start the server
server.serve_forever()
```

同样的也是在当前目录下建立一个 HTTP 服务器，默认认为在 cgi-bin 和 ht-bin 目录下中的文件为 CGI 脚本文件，而其他地方的文件为静态文件。

我们来创建 index.html 提交一个表单到 cgi-bin/post.py 中。

index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>CGI-FORM</title>
</head>
<body>
	<img src="image1.png" alt="image">
	<form action="cgi-bin/post.py" method="post">
		<label for="name">Name:</label>
		<input type="text" name="name">
		<input type="submit" value="Submit">
	</form>
</body>
</html>
```

post.py

```python
# coding=utf-8

import cgi

form = cgi.FieldStorage()

# Output to stdout, CGIHttpServer will take this as response to the client
print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers
print "<p>Hello world!</p>"         # Start of content
print "<p>" +  repr(form['name']) + "</p>"
print "<p>" +  form.getvalue('name') + "</p>"


```

form.getvalue() 方法可以接受 GET 请求或者是 POST 请求。