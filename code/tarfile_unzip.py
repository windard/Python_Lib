#coding=utf-8

import tarfile 

#解压到当前文件夹
#此处也可以直接用g.extractall()
g = tarfile.open('demo.tar.gz','r:gz')
for i in g.getnames():
	g.extract(i)
