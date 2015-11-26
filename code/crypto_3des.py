#coding=utf-8

from Crypto.Cipher import DES3
import base64

#三重DES加密的密钥是16位的
key = "0123456789abcdef"
IV = "abcdefgl"

#明文
text = "helloworld111111"
c = DES3.new(key,DES3.MODE_CBC,IV)
cipher = c.encrypt(text)
results = base64.b64encode(cipher)
print results

#解密
m = DES3.new(key,DES3.MODE_CBC,IV)
cipher = base64.b64decode(results)
plain = m.decrypt(cipher)
print plain
