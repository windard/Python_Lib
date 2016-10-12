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