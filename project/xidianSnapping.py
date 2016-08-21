#coding=utf-8

import sys
import time
import smtplib
import MySQLdb
from email.mime.text import MIMEText
import logging
import requests
from bs4 import BeautifulSoup

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

class Database(object):
    """docstring for Database"""
    def __init__(self, host="localhost",user="root",password="",db="",port=3406,charset="utf8"):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.charset = charset
        self.db = db
        try:
            self.conn = MySQLdb.connect(host=self.host,user=self.user,passwd=self.password,db=self.db,port=self.port,charset=self.charset)
            self.cur = self.conn.cursor()
            self.cur.execute('SET NAMES utf8;')
            self.cur.execute('SET CHARACTER SET utf8;')
            self.cur.execute('SET character_set_connection=utf8;')
        except Exception,e:
            print e

    def exec_(self,query):
        try:
            self.cur.execute(query)
            result = {"code":"00","content":[]}
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
            return {"code":"01","content":tuple(e)}

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
                    where.append("%s='%s'"%(str(key),str(value)))
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
                    limit = " LIMIT "+str(option.get("limit"))
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
                where.append("%s='%s'"%(str(key),str(value)))
            conds = []
            for key,value in values.items():
                conds.append("%s='%s'"%(str(key),str(value)))
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
                where.append("%s='%s'"%(str(key),str(value)))
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

logger = logging.getLogger("Xidian Grade")
formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(lineno)-4d %(message)s', '%Y%b%d %a %H:%M:%S',)

file_handler = logging.FileHandler("XidianGrade.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)

logger.setLevel(logging.DEBUG)

logger.info("Start Snapping")

class XidianGrade(object):
    """docstring for XidianGrade"""
    def __init__(self):
        self.s = requests.Session()

    def login(self):
        url = "http://ids.xidian.edu.cn/authserver/login?service=http%3A%2F%2Fjwxt.xidian.edu.cn%2Fcaslogin.jsp"
        Host = 'ids.xidian.edu.cn'

        Accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        AcceptLanguage = 'zh-CN,zh;q=0.8'
        Connection = 'keep-alive'
        AcceptEncoding = 'gzip, deflate, sdch'
        CacheControl = 'max-age=0'
        UserAgent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'

        self.headers = {'Accept':Accept,'Accept-Encoding':AcceptEncoding, 'Accept-Language':AcceptLanguage,'Cache-Control':CacheControl,'Connection':Connection,'Upgrade-Insecure-Requests':1,'User-Agent':UserAgent,}

        page = self.s.get(url=url,headers=self.headers)
        html = page.content

        logger.info("Received Logging Page")

        soup = BeautifulSoup(html)

        data = {}

        inputs = soup.find_all("input")

        try:
            for i in inputs:
                data[i.attrs['name']]=i.attrs['value']
        except Exception,e:
            logger.warning("Get Wrong Page")
            # print html
            sys.exit(0)

        data['username']="XXXXXX"
        data['password']="XXX"
        url = "http://ids.xidian.edu.cn/authserver/login?service=http%3A%2F%2Fjwxt.xidian.edu.cn%2Fcaslogin.jsp"
        page = self.s.post(url=url,headers=self.headers,data=data)
        html = page.content

        logger.info("Login Success")

    def getGrade(self):
        gradeutl = "http://jwxt.xidian.edu.cn/gradeLnAllAction.do?type=ln&oper=qbinfo&lnxndm=2015-2016%D1%A7%C4%EA%B5%DA%B6%FE%D1%A7%C6%DA(%C1%BD%D1%A7%C6%DA)"

        page = self.s.get(url=gradeutl,headers=self.headers)
        html = page.content

        logger.info("Get Grade")

        self.grade = BeautifulSoup(html)

    def run(self):
        try:
            self.database = Database(password="XXXXXX",db="feed")
        except Exception,e:
            logger.error("MySQL Connect Failed")

        tables = {0:'dayishang',1:'dayixia',2:'daershang',3:'daerxia',4:'dasanshang',5:'dasanxia',6:'dasishang',7:'dasixia'}
        # gr = open("grade.txt","w")
        allgrades = self.grade.find_all("td",class_="pageAlign")
        for item in enumerate(allgrades):
            first = True
            logger.info("Now Start Check Term "+tables[item[0]])
            for each in item[1].findChildren("tr"):
                if first:
                    first = False
                else:
                    eachclass = {}
                    # gr.write("-----------------------------------------------\n")
                    try:
                        eachclass['num'] = each.findChildren("td")[0].get_text().encode("utf-8").replace(" ","").replace("\n","").replace("\t","").replace("\r","")
                        # gr.write(eachclass['num'])
                        # gr.write("\n")
                        eachclass['name'] = each.findChildren("td")[2].get_text().encode("utf-8").replace(" ","").replace("\n","").replace("\t","").replace("\r","")
                        # gr.write(eachclass['name'])
                        # gr.write("\n")
                        eachclass['xuefen'] = each.findChildren("td")[4].get_text().encode("utf-8").replace(" ","").replace("\n","").replace("\t","").replace("\r","")
                        # gr.write(eachclass['xuefen'])
                        # gr.write("\n")
                        eachclass['grade'] = each.findChildren("td")[6].get_text().encode("utf-8").replace(" ","").replace("\n","").replace("\t","").replace("\r","")
                        # gr.write(eachclass['grade'])
                        # gr.write("\n")
                        tablenum = self.database.get(tables[item[0]],["count(*)"])["content"][0]
                        if  tablenum == len(item[1].findChildren("tr"))-2:
                            logger.info("%s term is enough"%tables[item[0]])
                            break
                        else:
                            if self.checkTbale(tables[item[0]],eachclass):
                                logger.info("One Grade Is Out")
                                self.database.new(tables[item[0]],[str(eachclass['num']),str(eachclass['name']),str(eachclass['xuefen']),str(eachclass['grade'])],["num","name","xuefen","grade"])
                                self.snedMail(eachclass,item[1])
                    except Exception,e:
                        # print e
                        pass

        # gr.close()
        logger.info("grade.txt Is ALL")

    def checkTbale(self,table,data):
        return False if  self.database.get(table,option={"where":{"num":str(data['num']),"name":str(data['name'])}})["content"] else True

    def snedMail(self,data,allgrade):
        content ="<h1>最新成绩出来了</h1>"+ \
        "<table>"+ \
        "<thead><tr><td>课程号</td><td>课程名</td><td>学分</td><td>成绩</td></tr></thead>"+ \
        "<tbody><tr><td>"+str(data['num'])+"</td><td>"+str(data['name'])+"</td><td>"+str(data['xuefen'])+"</td><td>"+str(data['grade'])+"</td></tr></tbody>"+ \
        "</table>"

        content += \
        "&nbsp;<hr>"+ \
        "<h1>总成绩</h1><table>"+ \
        "<thead><tr><td>课程号</td><td>课程名</td><td>学分</td><td>成绩</td></tr></thead>"+ \
        "<tbody>"

        first = True
        for each in allgrade.findChildren("tr"):
            if first:
                first = False
            else:
                eachclass = {}
                try:
                    eachclass['num'] = each.findChildren("td")[0].get_text().encode("utf-8").replace(" ","").replace("\n","").replace("\t","").replace("\r","")
                    content+="<tr><td>"+eachclass['num']
                    eachclass['name'] = each.findChildren("td")[2].get_text().encode("utf-8").replace(" ","").replace("\n","").replace("\t","").replace("\r","")
                    content+="</td><td>"+eachclass['name']
                    eachclass['xuefen'] = each.findChildren("td")[4].get_text().encode("utf-8").replace(" ","").replace("\n","").replace("\t","").replace("\r","")
                    content+="</td><td>"+eachclass['xuefen']
                    eachclass['grade'] = each.findChildren("td")[6].get_text().encode("utf-8").replace(" ","").replace("\n","").replace("\t","").replace("\r","")
                    content+="</td><td>"+eachclass['grade']+"</tr>"
                except Exception,e:
                    content = content[:content.rfind("<tr>")]
                    content+="</tbody></table><hr>"+each.get_text().encode("utf-8").replace(" ","").replace("\n","").replace("\t","").replace("\r","")

        self.mailcontrol = MailControl(username="18607571914@163.com",password="XXXXXX")
        logger.info("Connecting to Mail Successful")

        try:
            if int(data['grade'][:2])>60:
                title = "太棒了，又过了一科"
            else:
                title = "妈的，竟然挂了？"
        except:
            title = data["grade"] + "一科"
        self.mailcontrol.setSubject(title)
        self.mailcontrol.setReceive("1106911190@qq.com")
        self.mailcontrol.setContent(content,"html")
        self.mailcontrol.send()
        logger.info("Send Mail Successful")

def main():
    xidiangrade = XidianGrade()
    xidiangrade.login()
    xidiangrade.getGrade()
    xidiangrade.run()

if __name__ == '__main__':
    n = 1
    while 1:
        logger.info("No.%d Snap Start"%n)
        main()
        n += 1
        time.sleep(60*3)
