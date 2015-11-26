#coding=utf-8

from pyDes import *
import base64

#DES的key和IV向量都是8位
#在多重DES加密中为8的倍数位
key = "01234567"
IV = "abcdefgl"

#IV =  b"\0\0\0\0\0\0\0\0"
#des(key, CBC, IV, pad=None, padmode=PAD_PKCS5)

#明文必须为16的倍数，否则需截断或填充
text = "helloworld111111"
c = des(key,CBC,IV)
cipytext = c.encrypt(text)

#密文
results = base64.b64encode(cipytext)
print results
#有时也用16进制加密
#results = cipytext.encode("hex")

#解密
m = des(key,CBC,IV)
cipytext = base64.b64decode(results)
plain = m.decrypt(cipytext)
print plain