# coding=utf-8

import time
import requests
from Logger import logger
from bs4 import BeautifulSoup
from Database import Database
from MailManager import MailControl

LOGIN_USERNAME = "XXX"
LOGIN_PASSWORD = "XXX"

DB_USERNAME = 'XXX'
DB_PASSWORD = 'XXX'

MAIL_USERNAME = 'XXX@163.com'
MAIL_RECEIVER = 'XXX@qq.com'
MAIL_PASSWORD = 'XXX'

def sendMail(data, allgrade):
    logger.info("Prepare Send Mail")

    mc = MailControl(username=MAIL_USERNAME, password=MAIL_PASSWORD)

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

    if int(data['grade'][:2]) > 60:
        title = "太棒了，又过了一科"
    else:
        title = "妈的，竟然挂了？"

    mc.setSubject(title)
    mc.setReceiver(MAIL_RECEIVER)
    mc.setContent(content, 'html')
    mc.send()

def main():
    logger.info("Start Snapping")
    s = requests.Session()

    url = "http://ids.xidian.edu.cn/authserver/login?service=http%3A%2F%2Fjwxt.xidian.edu.cn%2Fcaslogin.jsp"
    Host = 'ids.xidian.edu.cn'

    Accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    AcceptLanguage = 'zh-CN,zh;q=0.8'
    Connection = 'keep-alive'
    AcceptEncoding = 'gzip, deflate, sdch'
    CacheControl = 'max-age=0'
    UserAgent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'

    headers = {'Accept':Accept, 'Accept-Encoding':AcceptEncoding, 'Accept-Language':AcceptLanguage, 'Cache-Control':CacheControl, 'Connection':Connection, 'User-Agent':UserAgent}

    page = s.get(url=url, headers=headers)
    html = page.content

    logger.info("Received Logging Page")

    soup = BeautifulSoup(html,"lxml")

    data = {}

    inputs = soup.find_all("input")

    try:
        for i in inputs:
            data[i.attrs['name']]=i.attrs['value']
    except Exception,e:
        print tuple(e)

    data['username'] = LOGIN_USERNAME
    data['password'] = LOGIN_PASSWORD

    url = "http://ids.xidian.edu.cn/authserver/login?service=http%3A%2F%2Fjwxt.xidian.edu.cn%2Fcaslogin.jsp"
    
    page = s.post(url=url,headers=headers,data=data)
    html = page.content

    logger.info("Login Success")

    gradeutl = "http://jwxt.xidian.edu.cn/gradeLnAllAction.do?type=ln&oper=qbinfo&lnxndm=2015-2016%D1%A7%C4%EA%B5%DA%B6%FE%D1%A7%C6%DA(%C1%BD%D1%A7%C6%DA)"

    page = s.get(url=gradeutl, headers=headers)
    html = page.content
    if len(html) < 1000:
        logger.info("Get Grade Failed")
        return False

    logger.info("Get Grade Success")
    
    grade = BeautifulSoup(html, "lxml")

    db = Database(user=DB_USERNAME, password=DB_PASSWORD)

    logger.info("Connect MySQL Success")

    db.exec_("use feed")

    databases = {0:'dayishang', 1:'dayixia', 2:'daershang', 3:'daerxia', 4:'dasanshang', 5:'dasanxia', 6:'dasishang', 7:'dasixia'}
    gr = open("grade.txt","a")
    allgrades = grade.find_all("td",class_="pageAlign")
    for item in enumerate(allgrades):
        first = True
        print >> gr, "-"*80
        for each in item[1].findChildren("tr"):
            if first:
                first = False
            else:
                eachclass = {}
                try:
                    tablenum = db.get(databases[item[0]], ["count(*)"])['content'][0]
                    if  tablenum == len(item[1].findChildren("tr"))-2:
                        logger.info("%s is enough"%databases[item[0]])
                        break
                    eachclass['name'] = each.findChildren("td")[2].get_text().encode("utf-8").replace(" ","").replace("\n","").replace("\t","").replace("\r","")
                    eachclass['num'] = each.findChildren("td")[0].get_text().encode("utf-8").replace(" ","").replace("\n","").replace("\t","").replace("\r","")
                    eachclass['xuefen'] = each.findChildren("td")[4].get_text().encode("utf-8").replace(" ","").replace("\n","").replace("\t","").replace("\r","")
                    eachclass['grade'] = each.findChildren("td")[6].get_text().encode("utf-8").replace(" ","").replace("\n","").replace("\t","").replace("\r","")[:-2]
                    print >> gr, "%s--%s--%s--%s"%(eachclass['num'], eachclass['name'], eachclass['xuefen'], eachclass['grade'])
                    if not db.get(databases[item[0]], ["count(*)"],{"where":{"num":eachclass['num'],"grade":eachclass['grade']}})['content'][0]:
                        db.new(databases[item[0]], eachclass.values(), ['grade', 'num', 'name', 'xuefen'])
                        logger.info("%s %s is Out"%(databases[item[0]], eachclass['name']))
                        sendMail(eachclass, item[1])
                        logger.info("Send Mail Success")
                except Exception,e:
                    # print tuple(e)
                    pass
    gr.close()
    logger.info("Snapping ends")
    return True

if __name__ == '__main__':
    while 1:
        if main():
            time.sleep(60*5)
        else:
            time.sleep(10)
