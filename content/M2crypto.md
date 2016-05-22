##M2crypto

这是一个很强大加密解密python库，用这个来实现rsa加密能够比使用rsa库更快一些。

```python
#coding=utf-8

from M2Crypto import RSA,BIO

rsa = RSA.gen_key(1024, 3, lambda *agr:None)
pub_bio = BIO.MemoryBuffer()
priv_bio = BIO.MemoryBuffer()

rsa.save_pub_key_bio(pub_bio)
rsa.save_key_bio(priv_bio, None)

pub_key = RSA.load_pub_key_bio(pub_bio)
priv_key = RSA.load_key_bio(priv_bio)

message = 'This is message'

encrypted = pub_key.public_encrypt(message, RSA.pkcs1_padding).encode("base64")
decrypted = priv_key.private_decrypt(encrypted.decode("base64"), RSA.pkcs1_padding)

print encrypted
print decrypted

```

同样也能用于aes加密

``` python
#coding=utf-8
from M2Crypto.EVP import Cipher
from M2Crypto import m2
from M2Crypto import util

ENCRYPT_OP = 1 # 加密操作
DECRYPT_OP = 0 # 解密操作

iv = '\0' * 16 # 初始化变量，对于aes_128_ecb算法无用
PRIVATE_KEY = 'dd7fd4a156d28bade96f816db1d18609' # 密钥

def Encrypt(data):
  '使用aes_128_ecb算法对数据加密'
  cipher = Cipher(alg = 'aes_128_ecb', key = PRIVATE_KEY, iv = iv, op = ENCRYPT_OP)
  buf = cipher.update(data)
  buf = buf + cipher.final()
  del cipher
  # 将明文从字节流转为16进制
  output = ''
  for i in buf:
    output += '%02X' % (ord(i))
  return output

def Decrypt(data):
  '使用aes_128_ecb算法对数据解密'
  # 将密文从16进制转为字节流
  data = util.h2b(data)
  cipher = Cipher(alg = 'aes_128_ecb', key = PRIVATE_KEY, iv = iv, op = DECRYPT_OP)
  buf = cipher.update(data)
  buf = buf + cipher.final()
  del cipher
  return buf

print Encrypt("This is a message")
```

还有md5加密

``` python
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
```
