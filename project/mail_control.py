#coding=utf-8

import smtplib
from email.mime.text import MIMEText


def send_mail(username, password, receive, subject, content, host="smtp.163.com", ssl=True):
    a = MailControl(username=username, password=password, host=host, ssl=ssl)
    a.setSubject(subject)
    a.setReceiver(receive)
    a.setContent(content)
    a.send()


class MailControl(object):
    """docstring for MailControl"""

    def __init__(self, username, password, host="smtp.163.com", ssl=True):
        """
            import mail_control
            a = mail_control.MailControl(username="18607571914@163.com",
                                        password="XXXXXX")
            a.setSubject("How Are You?")
            a.setReceiver("1106911190@qq.com")
            a.setContent("这是我给你的爱")
            a.send()
        """
        self.host = host
        self.username = username
        self.password = password
        self.subject = None
        self.receive = None
        self.message = None
        self.smtpObj = smtplib.SMTP(self.host)
        if ssl:
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


if __name__ == '__main__':

        a = MailControl(username="18607571914@163.com", password="XXXXXX")
        a.setSubject("How Are You?")
        a.setReceiver("1106911190@qq.com")
        a.setContent("这是我给你的爱")
        a.send()
