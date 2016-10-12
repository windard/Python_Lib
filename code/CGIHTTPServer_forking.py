# coding=utf-8

from BaseHTTPServer import HTTPServer
from CGIHTTPServer import CGIHTTPRequestHandler
from SocketServer import ForkingMixIn

class ForkingServer(ForkingMixIn,HTTPServer):
	pass

serveraddr = ('',9876)
srvr = ForkingServer(serveraddr,CGIHTTPRequestHandler)
srvr.serve_forever()
