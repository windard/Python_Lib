#coding=utf-8

import time
import sqlite3
import smtplib
import logging
import feedparser
from email.mime.text import MIMEText

logger = logging.getLogger("FeedGrab Logging")
formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(lineno)-4d %(message)s', '%Y %b %d %a %H:%M:%S',)

file_handler = logging.FileHandler("feedgrab.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

logger.setLevel(logging.DEBUG)

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

    def get(self,table,filed=["*"],option={}):
        try:
            if "*" in filed:
                filed = "*"
            else:
                filed = ",".join(filed)
            conds = ""
            if option.get("where",""):
                where = []
                for key,value in option.get("where").items():
                    where.append("%s='%s'"%(unicode(key),unicode(value)))
                conds += "WHERE "
                conds += " AND ".join(where)
            if option.get("order",""):
                order = ""
                order += " ORDER BY "+ option.get("order")[0]
                if len(option.get("order")) == 2:
                    order += " "+option.get("order")[1]
                conds += order
            if option.get("limit",""):
                limit = ""
                if type(option.get("limit")) == str:
                    limit = " LIMIT "+unicode(option.get("limit"))
                else:
                    limit = " LIMIT " + ",".join(option.get("limit"))
                conds += limit
            return self.exec_("SELECT %s FROM %s %s"%(filed,table,conds))
        except Exception,e:
            return {"code":"02","content":tuple(e)}

    def set(self,table,values,option={}):
        try:
            where = []
            for key,value in option.items():
                where.append("%s='%s'"%(unicode(key),unicode(value)))
            conds = []
            for key,value in values.items():
                conds.append("%s='%s'"%(unicode(key),unicode(value)))
            if len(where):
                return self.exec_("UPDATE %s SET %s WHERE %s"%(table," AND ".join(conds)," AND ".join(where)))
            else:
                return self.exec_("UPDATE %s SET %s "%(table," AND ".join(conds)))
        except Exception,e:
            return {"code":"03","content":tuple(e)}

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

    def del_(self,table,option={}):
        try:
            where = []
            for key,value in option.items():
                where.append("%s='%s'"%(unicode(key),unicode(value)))
            if where:
                return self.exec_("DELETE FROM %s WHERE %s"%(table," AND ".join(where)))
            else:
                return self.exec_("DELETE FROM %s"%table)
        except Exception,e:
            return {"code":"05","content":tuple(e)}

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

class FeedGrab(object):
    """docstring for FeedGrab"""
    def __init__(self, url,db,username,password,receive):
        self.url = url
        self.db = Database(db)
        self.content = ""
        self.flag = 0
        self.username = username
        self.password = password
        self.receive = receive
        self.mc = MailControl(self.username,self.password)

    def run(self):
        logger.info("Start FeedGrab ... ")
        try:
            data = feedparser.parse(self.url)
        except feedparser.Error,e:
            logger.error("Connecting to Feed Failed %s" %e.args[1])
        else:
            logger.info("Receiving Feed Successful")
            for entry in data.entries:
                temp = self.db.get("homework",option={"where":{"title":entry.title,"content":entry.description}})
                if not int(temp["code"]) and not temp["content"]:
                    self.db.new("homework",[unicode(entry.title),unicode(entry.link),unicode(entry.published),unicode(entry.description)])
                    logger.info("One New Article")
                    self.content +="<a href =\""+entry.link+"\" >"+"<h1>"+entry.title+"</h1>"+"</a>"
                    self.content += entry.description
                    self.content += "<br />"
                    self.flag = 1
            if self.flag :
                try:
                    self.mc.setSubject(data.feed.title)
                    self.mc.setReceive(self.receive)
                    self.mc.setContent(self.content,"HTML")
                    self.mc.send()
                except Exception, e:
                    logger.error("Send Mail Failed")
                else:
                    logger.info("Sending Mail Successful")
            else :
                logger.info("Today Has Nothing new")
        finally:
            logger.info("End FeedGrab")

if __name__ == '__main__':
    fg = FeedGrab("http://1418019.top/atom.xml","homework.db","18607571914@163.com","XXXXXXS","1106911190@qq.com")
    fg.run()
    time.sleep(60*60)

