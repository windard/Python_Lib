## ping

服务器上最常见的网络命令，测试网络是否通畅，能否抵达目标。

一般用来根据能否 ping 通来判断自身的网络连接或者目标的网络连接，根据 ping 的时长来检测网络连接状况。

ping 使用 ICMP(internet control message protocol) 协议，不在 TCP/IP 协议层中，所以没有特定的端口号，如果强行使用 socket 连接，可以设置端口号为 1.

在七层网络模型中，icmp 是第三层协议，TCP/UDP 是第四层协议。

[An ICMP Reference](https://danielmiessler.com/study/icmp/)

如果使用 ping 命令来判断是否网络通畅

```
import os

status = os.system("ping -c 1 www.baidu.com");

if status == 0:
    print '连接成功!';
else:
    print '连接失败';

```

或者使用 ping 这个 python 库

```
# -*- coding: utf-8 -*-

import sys
import ping
import socket


def ping_test(host):
    try:
        ping.quiet_ping(host, count=1)
    except socket.error:
        return False
    else:
        return True


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print """
        Uasge: python ping_test.py baidu.com

        """
        sys.exit(0)
    print ping_test(sys.argv[1])

```

使用时需注意使用 root 权限运行。
