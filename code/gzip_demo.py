#coding=utf-8

import gzip

filename = open('zipfile_demo.py','rb')

#创建一个新的压缩文件
g = gzip.open('zipfile_demo.gz','wb')
g.write(filename.read())
filename.close()
g.close()

#打开一个已经创建的压缩文件
a = gzip.GzipFile('zipfile_demo.gz','ab')
a.write("This is another data")
a.close()

