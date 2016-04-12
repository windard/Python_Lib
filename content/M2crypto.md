##M2crypto

这是一个很强大加密解密python库，用这个来实现rsa加密能够比使用rsa库更快一些。

```python
#coding=utf-8

from M2Crypto import RSA

rsa = RSA.gen_key(1024, 3, lambda *agr:None)
pub_bio = BIO.MemoryBuffer()
priv_bio = BIO.MemoryBuffer()

rsa.save_pub_key_bio(pub_bio)
rsa.save_key_bio(priv_bio, None)

pub_key = RSA.load_pub_key_bio(pub_bio)
priv_key = RSA.load_key_bio(priv_bio)

message = 'This is message'

encrypted = pub_key.public_encrypt(message, RSA.pkcs1_padding)
decrypted = priv_key.private_decrypt(encrypted, RSA.pkcs1_padding)

print encrypted
print decrypted

```