# coding=utf-8
# Author: Windard
# Date: 2016-09-13

import os
import time
import requests

def main():
    s = requests.session()

    Accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    AcceptLanguage = 'zh-CN,zh;q=0.8'
    Connection = 'keep-alive'
    AcceptEncoding = 'gzip, deflate, sdch'
    UserAgent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'
    CacheControl = "no-cache"

    headers = {'Accept':Accept,'Accept-Encoding':AcceptEncoding, 'Accept-Language':AcceptLanguage,'Cache-Control':CacheControl,'Connection':Connection,'Upgrade-Insecure-Requests':1,'User-Agent':UserAgent}
    cookies = {'lzstat_uv':'26132910522086874288|3401870','Q8qA_2132_home_readfeed':'1451974353','safedog-flow-item':'D03A04C9E0C6AEE0012E35A1711D7B35','Q8qA_2132_saltkey':'R4W9F4xS',
    			'Q8qA_2132_lastvisit':'1474194784','Q8qA_2132_lastcheckfeed':'293064%7C1474198635','Q8qA_2132_auth':'2763GES0S%2BIQXkWSov0BrnlEl%2BtfDi8fv4mp9YzxR7wM%2BhZp6HYUr%2BJHpJL%2BX6Dlkbp%2FXlbxRF%2FXc7hSyo9%2FT9zBOIE',
    			'Q8qA_2132_visitedfid':'72D548D94','Q8qA_2132_smile':'1D1','Q8qA_2132_myrepeat_rr':'R0','Q8qA_2132_ulastactivity':'41e6bvBPYoVv5R3VUkWlwh4elzVajNuxCU5IjcvLqw8wJ5jNlHVW',
    			'Q8qA_2132_lip':'10.170.68.194%2C1473742408','Q8qA_2132_sid':'L16WIP','Q8qA_2132_sendmail':'1','Q8qA_2132_checkpm':'1','Q8qA_2132_lastact':'1474716045%09misc.php%09patch',
                'Q8qA_2132_nofavfid':"1",'Q8qA_2132_viewid':'tid_811404'}


    url = "http://rs.xidian.edu.cn/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&inajax=1"

    data = {"formhash":"0aa655c7","qdxq":"yl","qdmode":"3","todaysay":"","fastreply":"0"}

    html = s.post(url,headers=headers,cookies=cookies,data=data)

    if html.content.decode("utf-8").find(u"签到成功") != -1:
        print "Successful !"

if __name__ == '__main__':
    while 1:
        main()
        time.sleep(60*60*24)
