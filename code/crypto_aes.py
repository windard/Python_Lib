#coding=utf-8

from Crypto.Cipher import AES
import base64

#设定一个密钥，密钥可以是是16位, 
#还可以是24 或 32 位长度，
#其对应为 AES-128, AES-196 和 AES-256.
key = '0123456789abcdef'
#设定加密模式
mode = AES.MODE_CBC
#设定加密密钥偏移IV量
IV = "abcdefghijklmnop"
encryptor = AES.new(key, mode,IV)

#明文,密文长度必须为16的倍数，否则需截断或填充
text = "hellodworld11111"
ciphertext = encryptor.encrypt(text)
#密文
results = base64.b64encode(ciphertext)
print results
#有时也会将结果进行十六进制转换
#print ciphertext.encode("hex")

#解密
decryptor = AES.new(key, mode,IV)
ciphertext = base64.b64decode(results)
plain = decryptor.decrypt(ciphertext)
print plain

