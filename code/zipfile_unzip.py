#coding=utf-8

import zipfile

#解压文件到当前文件夹
f = zipfile.ZipFile('test.zip','r')

#这一步为了保存压缩文件的目录结构
#此处也可以直接用g.extractall()
for i in f.namelist():
	f.extract(i)

#解压文件到指定文件夹
for i in f.namelist():
	f.extract(i,'demo')
