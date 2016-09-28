# coding=utf-8

import os
import time
import sqlite3
import smtplib
import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText

class Database(object):
    """docstring for Database"""
    def __init__(self, db=":memory:"):
        self.db = db
        try:
            self.conn = sqlite3.connect(self.db)
            self.cur = self.conn.cursor()
        except Exception,e:
            print e

    def exec_(self,query):
        try:
            self.cur.execute(query)
            result = {"code":"00","content":[]}
            self.conn.commit()
            for x in self.cur.fetchall():
                if len(x)==1:
                    result["content"].append(x[0])
                else:
                    children = []
                    for y in x:
                        children.append(y)
                    result["content"].append(children)
            return result
        except Exception,e:
            result = {"code":"01","content":tuple(e)}
            return result

    def new(self,table,values,option=[]):
        try:
            conds = ""
            for i in values:
                if type(i) == int:
                    conds += " %d,"
                else:
                    conds += " '%s',"
            if option:
                return self.exec_("INSERT INTO %s(%s) VALUES(%s)"%(table," , ".join(option),conds[:-1]%(tuple(values))))
            else:
                return self.exec_("INSERT INTO %s VALUES(%s)"%(table,conds[:-1]%(tuple(values))))
        except Exception,e:
            return {"code":"04","content":tuple(e)}

    def __del__(self):
        try:
            self.conn.commit()
            self.cur.close()
            self.conn.close()
        except Exception,e:
            print e

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
        except Exception,e:
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

class ExchangeMonitor(object):
	"""docstring for ExchangeMonitor"""
	def __init__(self, level, db, username, password, receive, exchange="Eur2Cny"):
		self.s = requests.session()
		self.level = level
		self.db = Database(db)
		self.exchange = exchange
		rules = {"Eur2Cny":"eurcny","Usd2Cny":"usdcny","Gbp2Cny":"gbpcny","Cny2Hkd":"cnyhkd","Cny2Jpy":"cnyjpy","Cny2Krw":"cnykrw"}
		self.url = "https://www.baidu.com/s?ie=UTF-8&wd="+rules[self.exchange]
		self.content = ""
		self.username = username
		self.password = password
		self.receive = receive
		self.mc = MailControl(self.username,self.password)

	def run(self):
		Accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
		AcceptLanguage = 'zh-CN,zh;q=0.8'
		Connection = 'keep-alive'
		AcceptEncoding = 'gzip, deflate, sdch'
		UserAgent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'
		CacheControl = "no-cache"

		headers = {'Accept':Accept,'Accept-Encoding':AcceptEncoding, 'Accept-Language':AcceptLanguage,'Cache-Control':CacheControl,'Connection':Connection,'Upgrade-Insecure-Requests':1,'User-Agent':UserAgent}

		html = self.s.get(self.url,headers=headers)

		soup = BeautifulSoup(html.content,'html.parser')

		price = soup.find_all('span','op-stockdynamic-cur-num')[0].getText()
		datetime = soup.find_all('div','op-stockdynamic-update')[0].getText().strip()[:19]

		self.db.new("monitor",[self.exchange,price,datetime])

		if float(price) <= self.level:
			self.content = u" 北京时间："+unicode(datetime)+u"，欧元只要 "+unicode(price)+u" 元人民币。"
			self.mc.setSubject(u"欧元降价了，原价七块的，八块的欧元，现价还是八块")
			self.mc.setReceive(self.receive)
			self.mc.setContent(self.content)
			self.mc.send()

def main():
	em = ExchangeMonitor(7.40,"exchangemonitor.db","18607571914@163.com","yang1106911190","1106911190@qq.com")
	em.run()

if __name__ == '__main__':
	""" Monitor Exchange For: Cny2Jpy, Eur2Cny, Cny2Krw, Usd2Cny, Gbp2Cny, Cny2Hkd """
	while 1:
		main()
		time.sleep(60*10)