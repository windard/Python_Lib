#coding=utf-8

import tarfile

allfile = []

#此处我们也使用之前zipfile的递归的方法
def getall(begindir):
	global allfile
	newpath = os.listdir(begindir)
	for i in newpath:
		currentpath = os.path.join(begindir,i)
		if os.path.isdir(currentpath):
			getall(currentpath)
		else:
			allfile.append(currentpath)

#创建一个tar.gz的压缩包
tar = tarfile.open('demo.tar.gz','w:gz')
for i in allfile:
	tar.add(i)

tar.close()
