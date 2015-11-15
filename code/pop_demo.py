#coding=utf-8

import poplib

#邮箱信息
host = "pop.163.com"
user = "18607571914@163.com"
password = "XXXXXX"
#连接邮件服务器
p = poplib.POP3(host)
p.user(user)
p.pass_(password)

#邮箱里邮件总的信息
status = p.stat()
print "MailBox has %d message for a total of %s bytes"%(status[0],status[1])
p.quit()