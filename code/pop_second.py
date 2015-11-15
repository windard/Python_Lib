#coding=utf-8

import poplib

#邮箱信息
host = "pop.163.com"
user = "18607571914@163.com"
password = "XXXXXX"
#连接邮件服务器
p = poplib.POP3(host)

#打印服务器欢迎信息
print p.getwelcome()

p.user(user)
p.pass_(password)

#邮箱里邮件总的信息
status = p.stat()
print "MailBox has %d message for a total of %s bytes"%(status[0],status[1])

#返回每个邮件的编号和大小
resp, mails, octets = p.list()
print mails

# 获取最新一封邮件, 注意索引号从1开始:
index = len(mails)
resp, lines, octets = p.retr(index)

print lines

#这样可以更加直观的查看邮件
msg_content = '\r\n'.join(lines)
print msg_content

#删除邮件
try:
	p.dele(index)
	print "Deleting Successful"
except:
	print "Deleting Failed"

p.quit()