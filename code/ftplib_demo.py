#coding=utf-8

import ftplib

#连接ftp服务器
f = ftplib.FTP('192.168.137.142')
#如果一开始只是构建ftp对象没有连接远程服务器的话，可以使用f.connect()来连接远程服务器

#打印ftp服务器的欢迎信息
print f.getwelcome()

#上面就是使用anonymous帐号匿名登录的
#如果使用帐号登录可以在上面加进去，也可以使用login函数
f.login('windard','windard')

#查看当前目录
print f.pwd()

#查看当前目录文件
print f.dir()

#进入ftp服务器上某一个文件夹
f.cwd('Desktop')

print f.dir()

f.quit()
