#coding=utf-8
import hashlib

#读取二进制文件
filename = open("md5_hash.py","rb")
filecontent = filename.read()

m = hashlib.md5()
m.update(filecontent)
decode = m.hexdigest()
print decode