#coding=utf-8

#先从简单的开始吧 MD5 SHA-1
from Crypto.Hash import MD5
from Crypto.Hash import SHA

m = MD5.new()
m.update("This is decode string")
print m.hexdigest()

h = SHA.new()
h.update("This is decode string")
print h.hexdigest()