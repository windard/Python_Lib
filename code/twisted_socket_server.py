# coding=utf-8

from time import ctime
from twisted.internet import protocol, reactor

port = 8099

class TSServProtocol(protocol.Protocol):
	def connectionMade(self):
		clnt = self.clnt = self.transport.getPeer().host
		print "... connected from:",clnt

	def dataReceived(self, data):
		self.transport.write('[%s] %s'%(ctime(), data))

factory = protocol.Factory()
factory.protocol = TSServProtocol
print "waiting for connection ..."
reactor.listenTCP(port,factory)
reactor.run()
