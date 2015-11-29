#coding=utf-8
import hashlib

#读取二进制文件
filename = open("md5_hash.py","rb")

block = 2**20

m = hashlib.md5()

while True:
	data = filename.read(block)
	if not data:
		break
	m.update(data)

decode = m.hexdigest()
print decode
