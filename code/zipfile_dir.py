#coding=utf-8

import zipfile
import os

allfile = []

#递归得到所有的文件，空文件夹则忽略不计
def getall(begindir):
	global allfile
	newpath = os.listdir(begindir)
	for i in newpath:
		currentpath = os.path.join(begindir,i)
		if os.path.isdir(currentpath):
			getall(currentpath)
		else:
			allfile.append(currentpath)

#需要压缩的文件夹
getall('test')

f = zipfile.ZipFile('test.zip','w',zipfile.ZIP_DEFLATED)
for i in allfile:
	f.write(i)

f.close()

