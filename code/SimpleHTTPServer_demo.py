# coding=utf-8

from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

serveraddr = ('',9876)
srvr = HTTPServer(serveraddr,SimpleHTTPRequestHandler)
srvr.serve_forever()
