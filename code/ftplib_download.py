#coding=utf-8

import ftplib

#设置缓存区大小
bufsize = 2048

def writeline(data):
	localfile2.write(data+'\n')

f = ftplib.FTP('localhost')
#这次以匿名身份登录
f.login()

print f.dir()

#以二进制格式下载非文本格式文件
#先创建本地文件
localfile1 = open('readme.tar.gz','wb')
f.retrbinary('RETR readme.tar.gz',localfile1.write,bufsize)
localfile1.close()

#以ASCII格式下载文本文件
localfile2 = open('readme.md','w')
f.retrlines('RETR readme.md',writeline)
localfile2.close()

f.quit()
