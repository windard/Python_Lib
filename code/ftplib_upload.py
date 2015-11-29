#coding=utf-8

import ftplib

f = ftplib.FTP('localhost')
f.login('windard','windard')

#以二进制格式上传
localfile1 = open('demo.tar.gz','rb')
f.storbinary('STOR demo.tar.gz',localfile1)
localfile1.close()

#以ASCII格式上传
localfile2 = open('demo.txt','r')
f.storlines('STOR demo.txt',localfile2)
localfile2.close()

f.quit()

