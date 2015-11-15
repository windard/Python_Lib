#coding=utf-8

import smtplib

#先创建一个连接邮件服务器对象，使用默认端口25
smtpObj = smtplib.SMTP("smtp.qq.com")
try:
	smtpObj.starttls()
	print "Successful SSL"
except:
	pass
#用户名和密码登陆
from_name = '1106911190@qq.com'
to_name = '18607571914@163.com'
#如果此处用的是QQ邮箱，那么这个密码就是你的QQ邮箱独立密码
password = 'XXXXXX'
#以下为邮件的内容,发送的内容是字符串。
#但是邮件一般由标题，发件人，收件人，邮件内容，附件构成。
#发送邮件的时候需要使用SMTP协议中定义的格式
message = """
From: From Person <1106911190@qq.com>
To: To Person <me@wenqiangyang.com>
Subject: SMTP e-mail test

日出东方，唯我不败
"""

#登陆邮箱
smtpObj.login(from_name,password)
#发送邮件
smtpObj.sendmail(from_name,to_name,message)
print "Sending Successful"
#关闭连接
smtpObj.close()