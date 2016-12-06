# coding=utf-8

import nmap 

nm = nmap.PortScanner()

nm.scan(hosts='10.170.1.158/24', arguments='-p 161 -sU')

hosts_list = [(x, nm[x][u'udp'][161]['state']) for x in nm.all_hosts()]
for host, status in hosts_list:
    print('{0}:{1}'.format(host, status))