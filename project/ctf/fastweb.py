#coding=utf-8

import requests
import re
from bs4 import BeautifulSoup

s = requests.Session()

url = "http://question4.erangelab.com/"
Host = 'question4.erangelab.com'
# Referer = 'http://burningcodes.net/ctf%e8%ae%ad%e7%bb%83%e8%90%a5%e4%b9%8b%e8%87%aa%e5%8a%a8%e6%8f%90%e4%ba%a4%e8%a1%a8%e5%8d%95/'

Accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
AcceptLanguage = 'zh-CN,zh;q=0.8'
Connection = 'keep-alive'
AcceptEncoding = 'gzip, deflate, sdch'
CacheControl = 'max-age=0'
UserAgent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'

# Cookie = {'wctf_think_language':'zh-CN','PHPSESSID':'h3l8403ppo6pkjfu0mohv8a370','Hm_lvt_184d7dcce9f76d1f5ab23d66e447d9a8':'1462670777,1462670945','Hm_lpvt_184d7dcce9f76d1f5ab23d66e447d9a8':'1462671596'}

headers = {'Accept':Accept,
            'Accept-Encoding':AcceptEncoding, 'Accept-Language':AcceptLanguage,'Cache-Control':CacheControl,'Connection':Connection,'Upgrade-Insecure-Requests':1,'User-Agent':UserAgent,}
page = s.get(url=url,headers=headers)
html = page.content

soup = BeautifulSoup(html)
text = soup.div.string
n = 0
for i in text:
    if i == '$':
        n += 1
# text = soup.hr.next

# text = soup.findall("$");
# text = soup.div
# string = text

# print text
# print type(text)

print text

w = len(re.findall('w',text))
o = len(re.findall('o',text))
l = len(re.findall('l',text))
d = len(re.findall('d',text))
y = len(re.findall('y',text))
# print "w:",w,"o:",o,"l:",l,"d:",d,"y:",y
data = str(w)+str(o)+str(l)+str(d)+str(y)

payload = {'anwser':'d0llars','submit':'submit'}
headers = {'Accept':Accept,'Accept-Encoding':AcceptEncoding, 'Accept-Language':AcceptLanguage,'Cache-Control':CacheControl,'Connection':Connection,'Upgrade-Insecure-Requests':1,'User-Agent':UserAgent,}
page = s.post(url=url+"check.php",data=payload,headers=headers)
html = page.content

print payload
print html
