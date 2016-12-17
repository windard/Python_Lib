## nmap 
有名的网络端口扫描工具，有大神为它写了一个 Python 库 python-nmap ，调用 nmap 来实现端口扫描。

nmap 的简单使用

- `-A` 详细参数，包括所有开放端口，端口提供服务，操作系统类型等。
- `--open` 只显示开放端口
- ` --system-dns` 使用系统的 DNS 服务器
- `--dns-servers` 自行设定 DNS 服务器
- `-oN|oX <filename>` 以正常格式 normal|XML 格式输出到文件
- `--spoof-mac <mac address>` 伪装你的 Mac 地址
- `-sU` UDP 端口扫描
- `-sn|sP` Ping 测试 ，可以 `nmap -sn 10.177.233.31/24` ，可以 `nmap -sn 10.177.233.1-255`
- `-PE/PP/PM` 使用ICMP echo, timestamp, and netmask 请求包发现主机
- `-sT` TCP 连接扫描，会在目标主机中有请求记录，这也是默认的扫描方式
- `-sA` TCP ACK 扫描，探查目标主机防火墙过滤情况
- `-sS` TCP SYN 扫描，只进行TCP三次握手的前两步，很少有系统计入日志，默认使用，需要root权限
- `-sF` TCP FIN 模式探查，不被目标主机计入日志
- `-sX` 圣诞树(Xmas Tree) 模式探查
- `-sV` 扫描端口时同时探测服务版本号等信息
- `-p <range>` 指定端口扫描 `-p22; -p1-65535; -p U:53,111,137,T:21-25,80,139,8080,S:9` 若不指定端口则扫描65535个端口，默认只扫1000个危险端口
- `-F`  使用快速扫描模式 Fast mode 进行扫描
- `-O` 进行操作系统类型探查
- `-S <IP_Address>` 伪造 IP地址进行扫描
- `-e <iface>` 使用指定的网卡进行扫描
- `--traceroute` 显示探查中经过的节点
- `-v` 显示扫描过程
- `-vv` 显示详细扫描过程
- `-T<n>` n range 0-5 扫描速度

检测局域网中各个主机 snmp 服务的开启情况

```
# coding=utf-8

import nmap 

nm = nmap.PortScanner()

nm.scan(hosts='10.170.1.158/24', arguments='-p 161 -sU')

hosts_list = [(x, nm[x][u'udp'][161]['state']) for x in nm.all_hosts()]
for host, status in hosts_list:
    print('{0}:{1}'.format(host, status))
```

本人也实现了一个简单的端口扫描器，在[这里](https://github.com/windard/Port_Scan)