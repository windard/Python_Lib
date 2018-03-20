#coding=utf-8

import smtplib
from email.mime.text import MIMEText

class MailControl(object):
    """docstring for MailControl"""

    def __init__(self, username, password, host="smtp.qq.com"):
        self.host = host
        self.username = username
        self.password = password
        self.subject = None
        self.receive = None
        self.message = None
        self.smtpObj = smtplib.SMTP(self.host)
        self.smtpObj.starttls()
        try:
            self.smtpObj.login(self.username, self.password)
        except smtplib.SMTPException as e:
            print(tuple(e))
            exit(0)

    def __del__(self):
        try:
            self.smtpObj.close()
        except smtplib.SMTPException as e:
            print(tuple(e))
            pass

    def setSubject(self, subject):
        self.subject = subject
        if self.message:
            self.message["Subject"] = self.subject

    def setReceiver(self, receive):
        self.receive = receive
        if self.message:
            self.message["To"] = self.receive

    def setContent(self, content, _type="plain", charset="utf-8"):
        self.message = MIMEText(content, _subtype=_type, _charset=charset)
        self.message["From"] = self.username
        if self.subject:
            self.message["Subject"] = self.subject
        if self.receive:
            self.message["To"] = self.receive

    def send(self):
        try:
            self.smtpObj.sendmail(self.username, self.receive,
                                  self.message.as_string())
        except smtplib.SMTPException as e:
            print(tuple(e))

"""

import mailcontrol

a = mailcontrol.MailControl(username="18607571914@163.com",password="XXXXXX")

a.setSubject("How Are You?")

a.setReceive("1106911190@qq.com")

a.setContent("这是我给你的信")

a.send()
"""
