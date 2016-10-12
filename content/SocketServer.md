## SocketServer

一个真正的 web 服务器。

像前面的 SimpleHTTPServer 都是小打小闹，并不能提供真正的 web 服务，而如果直接使用 socket ，那么又过于复杂，所以有一个直接可以用来做 web 服务器的标准库，在提供一些基础的 web 服务函数之外，还可以自定义一些其他的服务。

### BaseHTTPServer 

```
# coding=utf-8

from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler

class RequestHandle(BaseHTTPRequestHandler):
	"""docstring for RequestHandle"""
	def _writeheaders(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers

	def do_HEAD(self):
		self._writeheaders()

	def do_GET(self):
		self._writeheaders()
		self.wfile.write("""
			<html>
				<head><title>Sample Page</title></head>
				<body>
					<h3>Hello World</h3>
					<p>This is a Sample HTML Page,Every Page this server provides will like this</p>
				</body>
			</html>
			""")

if __name__ == '__main__':
	serveraddr = ('',6789)
	srvr = HTTPServer(serveraddr, RequestHandle)
	srvr.serve_forever()
```

这是一个最基础 Web 服务器，监听 0.0.0.0:6789。它只能够响应 GET 请求，而且无论请求的是什么，返回值都是一样的。

调用 do_XXX 来监听 GET，HEAD 或者 POST 请求。

接下来我们试一下响应不同的请求。

```
# coding=utf-8

from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
import time

starttime = time.time()

class RequestHandler(BaseHTTPRequestHandler):

	def _writeheaders(self,doc):
		if doc is None:
			self.send_response(404)
		else:
			self.send_response(200)

		self.send_header('Content-type','text/html')
		self.end_headers()

	def _getdoc(self,filename):
		global starttime
		if filename == '/':
			return """
				<html>
					<head><title>Home Page</title></head>
					<body>
						<h3>This is Home Page</h3>
						<p>Home Page Like This and Nobody Care</p>
					</body>
				</html>
			"""
		elif filename == '/stats.html':
			return """
				<html>
					<head><title>Statistics</title></head>
					<body>
						<h3>This is Statistics Page</h3>
						<p>This server has been running for %d seconds</p>
					</body>
				</html>
			"""%int(time.time()-starttime)
		elif filename == '/headers':
			result = ""
			for header in self.headers:
				result += header+":"+self.headers.get(header)+"<br />"
			return result
		else:
			return None

	def do_HEAD(self):
		doc = self._getdoc(self.path)
		self._writeheaders(doc)

	def do_GET(self):
		doc = self._getdoc(self.path)
		self._writeheaders(doc)
		# time.sleep(10)
		if doc is None:
			self.wfile.write("""
					<html>
						<head><title>No Found</title></head>
						<body>
							This requested document '%s' was no found 
						</body>
					</html>
				"""%self.path)
		else:
			self.wfile.write(doc)

serveraddr = ('',7890)
srvr = HTTPServer(serveraddr,RequestHandler)
srvr.serve_forever()

```

这个 web 服务器能够做根据 不同的请求 返回 不同的数据 了，虽然还是显得有些简陋，但是也是可以使用的，还能够返回 404 错误。

这个 web 服务器还有一个严重的问题，就是它只能同时响应一个请求，虽然你可以连续打开一个又一个的页面，但是其实一个页面打开成功之后，即使是返回 404 页面，但是也是表明整个请求已经结束。

如果一个请求迟迟不能结束，或者有网页占用网络请求，那么另一个页面就会无法打开。可以在 do_GET 的方法中，使用 time.sleep() 来加长一个页面的时间，然后再打开另一个页面，这时你就会发现另一个页面会等到前一个页面加载完成之后再加载。

一般有两个简单的方法来解决这个问题，多线程 (forking) 或多进程 (threading) ，或者采用非阻塞式异步通信 (asynchronous)等办法。

我们来试一下使用多线程来解决这个问题。

```
# coding=utf-8

from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import time,threading

starttime = time.time()

class RequestHandler(BaseHTTPRequestHandler):

	def _writeheaders(self,doc):
		if doc is None:
			self.send_response(404)
		else:
			self.send_response(200)

		self.send_header('Content-type','text/html')
		self.end_headers()

	def _getdoc(self,filename):
		global starttime
		if filename == '/':
			return """
				<html>
					<head><title>Home Page</title></head>
					<body>
						<h3>This is Home Page</h3>
						<p>Home Page Like This and Nobody Care</p>
					</body>
				</html>
			"""
		elif filename == '/stats.html':
			return """
				<html>
					<head><title>Statistics</title></head>
					<body>
						<h3>This is Statistics Page</h3>
						<p>This server has been running for %d seconds</p>
					</body>
				</html>
			"""%int(time.time()-starttime)
		else:
			return None

	def do_HEAD(self):
		doc = self._getdoc(self.path)
		self._writeheaders(doc)

	def do_GET(self):
		print "Handling with thread",threading.currentThread().getName()
		doc = self._getdoc(self.path)
		self._writeheaders(doc)
		time.sleep(10)
		if doc is None:
			self.wfile.write("""
					<html>
						<head><title>No Found</title></head>
						<body>
							This requested document '%s' was no found 
						</body>
					</html>
				"""%self.path)
		else:
			self.wfile.write(doc)

class ThreadingHTTPServer(ThreadingMixIn,HTTPServer):
	pass

serveraddr = ('',7890)
srvr = ThreadingHTTPServer(serveraddr,RequestHandler)
srvr.serve_forever()

``` 

虽然增加了线程，但是感觉效果不明显，试一下多进程。

```
# coding=utf-8

from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
from SocketServer import ForkingMixIn
import time,os

starttime = time.time()

class RequestHandler(BaseHTTPRequestHandler):

	def _writeheaders(self,doc):
		if doc is None:
			self.send_response(404)
		else:
			self.send_response(200)

		self.send_header('Content-type','text/html')
		self.end_headers()

	def _getdoc(self,filename):
		global starttime
		if filename == '/':
			return """
				<html>
					<head><title>Home Page</title></head>
					<body>
						<h3>This is Home Page</h3>
						<p>Home Page Like This and Nobody Care</p>
					</body>
				</html>
			"""
		elif filename == '/stats.html':
			return """
				<html>
					<head><title>Statistics</title></head>
					<body>
						<h3>This is Statistics Page</h3>
						<p>This server has been running for %d seconds</p>
					</body>
				</html>
			"""%int(time.time()-starttime)
		else:
			return None

	def do_HEAD(self):
		doc = self._getdoc(self.path)
		self._writeheaders(doc)

	def do_GET(self):
		print "Handling with forking",os.getpid()
		doc = self._getdoc(self.path)
		self._writeheaders(doc)
		time.sleep(10)
		if doc is None:
			self.wfile.write("""
					<html>
						<head><title>No Found</title></head>
						<body>
							This requested document '%s' was no found 
						</body>
					</html>
				"""%self.path)
		else:
			self.wfile.write(doc)

class ForkingHTTPServer(ForkingMixIn,HTTPServer):
	pass

serveraddr = ('',7890)
srvr = ForkingHTTPServer(serveraddr,RequestHandler)
srvr.serve_forever()

```

多进程在 Windows 下无法使用。

### SimpleHTTPServer

简单的 SimpleHTTPServer 服务器，可以查看当前目录下文件。

```
# coding=utf-8

from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

serveraddr = ('',9876)
srvr = HTTPServer(serveraddr,SimpleHTTPRequestHandler)
srvr.serve_forever()

```

非常简单的服务器，也可以使用多线程的版本。

```
# coding=utf-8

from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import ThreadingMixIn

class ThreadingServer(ThreadingMixIn,HTTPServer):
	pass
	
serveraddr = ('',9876)
srvr = ThreadingServer(serveraddr,SimpleHTTPRequestHandler)
srvr.serve_forever()

```

### CGIHTTPServer

```
# coding=utf-8

from BaseHTTPServer import HTTPServer
from CGIHTTPServer import CGIHTTPRequestHandler
from SocketServer import ForkingMixIn

class ForkingServer(ForkingMixIn,HTTPServer):
	pass

serveraddr = ('',9876)
srvr = ForkingServer(serveraddr,CGIHTTPRequestHandler)
srvr.serve_forever()

```

这是一个多进程的 CGIHTTPServer ，同样的在 Windows 下运行不了。

CGI 服务器是现代服务器端脚本语言的基础，只要在当前目录下的 cgi-bin 或 ht-bin 目录下中的文件创建 CGI 脚本文件，就可以提供较为复杂的 web 服务。

### TCPServer

在前面的代码中已经可以看到这里的一些的常用类的层级关系。

```
CLASSES
    SocketServer.BaseRequestHandler
        SocketServer.DatagramRequestHandler
        SocketServer.StreamRequestHandler
            BaseHTTPServer.BaseHTTPRequestHandler
            	SimpleHTTPServer.SimpleHTTPRequestHandler
            		CGIHTTPServer.CGIHTTPRequestHandler
    SocketServer.BaseServer
        SocketServer.TCPServer
            BaseHTTPServer.HTTPServer
            SocketServer.UDPServer
            	SocketServer.ThreadingUDPServer
            	SocketServer.ForkingUDPServer
            SocketServer.ThreadingTCPServer
            SocketServer.ForkingTCPServer
	SocketServer.ThreadingMixIn
		SocketServer.ThreadingTCPServer
		SocketServer.ThreadingUDPServer
	SocketServer.ForkingMixIn
		SocketServer.ForkingUDPServer
		SocketServer.ForkingTCPServer
```

可以发现主要的基类都是在 SocketServer 里的，几乎所有的服务器类都是基于这个库里面的几个基类。

那我们就可以直接使用这个库里的基类，来实现一下我们自己的服务器协议。

```
# coding=utf-8

from SocketServer import ThreadingMixIn,TCPServer,StreamRequestHandler
import time

class TimeRequestHandler(StreamRequestHandler):
	def handle(self):
		print '[%s] -- connected from:%s'%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),self.client_address)
		req = self.rfile.readline().strip()
		if req == "asctime":
			result = time.asctime()
		elif req == "seconds":
			result = str(int(time.time()))
		elif req == "rfc822":
			result = time.strftime("%a, %d %b %Y %H:%M:%S +0000",time.gmtime())
		else:
			result = """
				Unhandled request. Send a line with one of the following words:
				asctime -- for human-readable time
				seconds -- seconds since the Unix Epoch
				rfc822 -- date/time in format used for mail and posts
			"""
		self.wfile.write(result+"\n")

class TimeServer(ThreadingMixIn,TCPServer):
	allow_reuse_address = 1

serveraddr = ('',8765)
srvr = TimeServer(serveraddr,TimeRequestHandler)
srvr.serve_forever()

```

这是一个简单的 时间服务器，使用 Telnet 连接并发送相应的字符，会按格式回复相应的时间。

如果想使用 IPv6 的话，在 TimeServer 类下添加 IPv6 的协议族 `address_family = socket.AF_INET6` 即可。