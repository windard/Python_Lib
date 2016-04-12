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