#coding=utf-8

from Crypto.Cipher import DES
import base64

key = "01234567"
IV = "abcdefgl"

#明文
text = "helloworld111111"
c = DES.new(key,DES.MODE_CBC,IV)
cipher = c.encrypt(text)
results = base64.b64encode(cipher)
print results

#解密
m = DES.new(key,DES.MODE_CBC,IV)
cipher = base64.b64decode(results)
plain = m.decrypt(cipher)
print plain
