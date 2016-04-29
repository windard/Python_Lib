#coding=utf-8

from M2Crypto.EVP import MessageDigest

def md5(buf): 
	b = MessageDigest('md5') 
	b.update(buf) 
	b.update('888') 
	c = b.digest() 
	s = '' 
	for i in c: s = s + '%02x' % ord(i) 
	return s

print md5("thisismessage")