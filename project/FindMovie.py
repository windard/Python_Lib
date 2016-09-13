# coding=utf-8
# Author: Windard
# Date: 2016-09-13

import codecs
import requests
import argparse
from bs4 import BeautifulSoup

def main(pages=5,cate=1):
    s = requests.session()

    Accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    AcceptLanguage = 'zh-CN,zh;q=0.8'
    Connection = 'keep-alive'
    AcceptEncoding = 'gzip, deflate, sdch'
    UserAgent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'
    CacheControl = "no-cache"

    headers = {'Accept':Accept,'Accept-Encoding':AcceptEncoding, 'Accept-Language':AcceptLanguage,'Cache-Control':CacheControl,'Connection':Connection,'Upgrade-Insecure-Requests':1,'User-Agent':UserAgent}
    cookies = {'lzstat_uv':'26132910522086874288|3401870','Q8qA_2132_home_readfeed':'1451974353','safedog-flow-item':'D03A04C9E0C6AEE0012E35A1711D7B35','Q8qA_2132_saltkey':'mCugguu4',
    			'Q8qA_2132_lastvisit':'1472340056','Q8qA_2132_lastcheckfeed':'293064%7C1472343673','Q8qA_2132_auth':'01fdDpJmghoUeHWIo%2Ftu2zezLTC%2F9rS1LWVwrKM7Fmb8JRJBcXjJ4kpoCxxv7ArNA14zua5Smj2HKIoN2w5aEVMg3U4',
    			'Q8qA_2132_visitedfid':'551D72D141D110D20D108D157D13D554D145','Q8qA_2132_smile':'16D1','Q8qA_2132_myrepeat_rr':'R0','Q8qA_2132_ulastactivity':'375dtmEp97ZVEG456H%2FxJ1WTpHtbMPJeCpeTYjh%2BIMBAUT9jXzT%2F',
    			'Q8qA_2132_lip':'10.170.68.194%2C1473742408','Q8qA_2132_sid':'iK355Z','Q8qA_2132_sendmail':'1','Q8qA_2132_checkpm':'1','Q8qA_2132_lastact':'1473742557%09misc.php%09patch'}

    for page in xrange(1,pages+1):
        movirurl = "http://rs.xidian.edu.cn/bt.php?mod=browse&t=all&page="+str(page)
        html = s.get(url=movirurl,headers=headers,cookies=cookies)

        soup = BeautifulSoup(html.content,'lxml')

        if page == 1:
            alltbodys = soup.find_all('tbody')[35:]
        else:
            alltbodys = soup.find_all('tbody')

        categories = {1:u'电影',2:u'剧集',3:u'音乐',4:u'动漫',5:u'游戏',6:u'综艺',7:u'体育',8:u'软件',9:u'学习',10:u'纪录片',11:u'西电',12:u'其他'}

        for tbody in alltbodys:
            if tbody.find_all('td')[1].getText()[1:3]==categories[cate]:
                f.write(tbody.find_all('td')[1].getText()+'------------')
                f.write(tbody.find_all('td')[3].getText()+'------------')
                if tbody.find_all('td')[5].find('span'):
                    f.write(tbody.find_all('td')[5].span['title']+'--------------')
                else:
                    f.write(tbody.find_all('td')[5].getText()+'--------------')
                f.write(tbody.find_all('td')[6].getText()+'\n\t\n')

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description="Find Resource In RS")
    # parser.add_argument("--pages",help="how many pages do you want to find",action="store",default=5,type=int)
    # parser.add_argument("--type",help="which type resource do you want to find ",action="store",default=1,type=int)
    # args = parser.parse_args()
    # pages = args.pages
    # filetype = args.type

    print unicode("请输入需要选取的页数","utf-8")
    pages = int(raw_input())
    print unicode("请选择需要选取的类型","utf-8")
    print unicode("0:全部,1:电影,2:剧集,3:音乐,4:动漫,5:游戏,6:综艺,7:体育,8:软件,9:学习,10:纪录片,11:西电,12:其他","utf-8")
    filetype = int(raw_input())

    with codecs.open('result.txt', 'w', "utf-8") as f:
        f.write(u"名称------------------------------------------------------------------------------------------------大小-----------发布时间------------------------种子数\n")
        if filetype:
            main(pages,filetype)
        else:
            for x in xrange(1,13):
                main(pages,x)
