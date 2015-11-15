#coding=utf-8

import poplib
import base64
import email
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

#邮箱信息
host = "pop.163.com"
user = "18607571914@163.com"
password = "yang1106911190"
p = poplib.POP3(host)

print p.getwelcome()

p.user(user)
p.pass_(password)

#邮箱里邮件总的信息
status = p.stat()
print "MailBox has %d message for a total of %s bytes"%(status[0],status[1])

#返回每个邮件的编号和大小
resp, mails, octets = p.list()
# print mails

# 获取最新一封邮件, 注意索引号从1开始:
index = len(mails)
resp, lines, octets = p.retr(index)

# print lines
# print type(lines)
# content1 = base64.b64decode(lines[-2])
# content2 = base64.b64decode(lines[-1])

#这样可以更加直观的查看邮件
msg_content = '\r\n'.join(lines)
# print msg_content
# print type(msg_content)
# print content1
# print content2

msg = Parser().parsestr(msg_content)
print msg
# print isinstance(msg,object)
if msg["Content-Transfer-Encoding"]:
	print msg["Content-Transfer-Encoding"]
else:
	pass

print msg["Data"]

#删除邮件
# try:
# 	p.dele(index)
# 	print "Deleting SUccessful"
# except:
# 	print "Deleting Failed"

p.quit()