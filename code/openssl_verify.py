# coding=utf-8

import socket, sys
from OpenSSL import SSL

cafile, host = sys.argv[1:]

def printx509(x509):
	fileds = {'country_name': 'Country',
			  'SP': 'State/Privince',
			  'L': 'Locality',
			  'O': 'Organization',
			  'OU': 'Organization Unit',
			  'CN': 'Common Name',
			  'email': 'E-Mail'}

	for filed, desc in fileds.items():
		try:
			print "%30s: %s"%(desc, getattr(x509, filed))
		except:
			pass

converified = 0

def verify(connection, cerificate, errnum, depth, ok):
	global cnverifield

	subject = cerificate.get_subject()
	issuer = cerificate.issuer()

	printx509(subject)

	printx509(issuer)

	if not ok:
		print "Could not verify cerificate"
		return 0

	if subject.CN == None or subject.CN.lower() != host.lower():
		print "Connected to %s, but get cert for %s"%(host, subject.CN)
	else:
		cnverifield = 1

	if depth == 0 and not cnverifield:
		print "Could not verify server name, failing"
		return 0

	print '-'*70
	return 1

ctx = SSL.Context(SSL.SSLv23_METHOD)
ctx.load_verify_locations(cafile) 

ctx.set_verify(SSL.VERIFY_PEER | SSL.VERIFY_FAIL_IF_NO_PEER_CERT, verify)

print "Creating socket ..."
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "Done"

ssl = SSL.Connection(ctx, s)

print "Establishing SSL ..."
ssl.connect(('www.openssl.org', 443))
print "Done"

print "Requesting document ..."
# ssl.sendall("GET / HTTP/1.0\r\n\r\n")
ssl.sendall("GET /\r\n") 
print "Done"

while 1:
	try:
		buf = ssl.recv(4096)
	except SSL.ZeroReturnError:
		break
	sys.stdout.write(buf)

ssl.close()

