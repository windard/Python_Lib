#coding=utf-8

import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

smtpObj = smtplib.SMTP("smtp.163.com")
from_name = '18607571914@163.com'
to_name = '1106911190@qq.com'
password = 'XXXXXX'

# 先创建一个带附件的对象
message = MIMEMultipart()

# 构造图像
image = MIMEImage(open('puzzle.jpg','rb').read())
image.add_header('Content-ID','<imagename>')

# 将图像加入邮件中
message.attach(image)

# 在邮件中加入内容
content = MIMEText("这是一封带有图有真相的邮件<br /><img src='cid:imagename'>","html","utf-8")
message.attach(content)

# 邮件的收件人，发件人及主题
message["Subject"] = "千秋万载，一统江湖"
message["From"] = from_name
message["To"] = to_name

smtpObj.login(from_name,password)
# 这个地方需要把message对象转化为字符串
smtpObj.sendmail(from_name,to_name,message.as_string())
print "Sending Successful"
smtpObj.close()