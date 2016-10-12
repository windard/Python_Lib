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
