#coding=utf-8

import smtplib
from email.mime.text import MIMEText

class MailControl(object):
    """docstring for MailControl"""
    def __init__(self,username,password,host="smtp.163.com"):
        self.host = host
        self.username = username
        self.password = password
        self.smtpObj = smtplib.SMTP(self.host)
        self.smtpObj.starttls()
        try:
            self.smtpObj.login(self.username,self.password)
        except smtplib.e:
            print e.args[1]

    def __del__(self):
        try:
            self.smtpObj.close()
        except:
            pass

    def setSubject(self,subject):
        self.subject = subject
        if hasattr(self,"message"):
            self.message["Subject"] = self.subject

    def setReceive(self,receive):
        self.receive = receive
        if hasattr(self,"message"):
            self.message["To"] = self.receive

    def setContent(self,content,_type="plain",charset="utf-8"):
        self.message = MIMEText(content,_subtype=_type,_charset=charset)
        self.message["From"] = self.username
        if hasattr(self,"subject"):
            self.message["Subject"] = self.subject
        if hasattr(self,"receive"):
            self.message["To"] = self.receive

    def send(self):
        try:
            self.smtpObj.sendmail(self.username,self.receive,self.message.as_string())
        except Exception,e:
            print e

"""

import mailcontrol

a = mailcontrol.MailControl(username="18607571914@163.com",password="XXXXXX")

a.setSubject("How Are You?")

a.setReceive("1106911190@qq.com")

a.setContent("这是我给你的信")

a.send()
"""
