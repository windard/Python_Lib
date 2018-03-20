## platform

获得各种系统信息版本号之类的。

1. platform.system() 操作系统名
4. platform.version() 操作系统版本号
4. platform.release() 操作系统内核信息
2. platform.dist() 操作系统发行信息
2. platform.uname() 相当于 uname 函数
4. platform.node() 操作系统用户名
4. platform.platform() 操作系统平台信息
4. platform.machine() 操作系统硬件类型标识符
4. platform.processor() 操作系统处理器
3. platform.architecture() 操作系统架构
4. platform._sys_version() python 使用的解释器
4. platform.java_ver() java 的环境变量
4. platform.python_version() python 的版本号
5. platform.python_implementation() python 的版本
4. platform.python_version_tuple() python 版本号的元组表示形式
4. platform.python_branch() python 的分支
4. platform.python_compiler() python 的编译器
4. platform.python_build() python 的解释器
4. platform.win32_ver() windows 的版本号
4. platform.mac_ver() mac 的版本号
4. platform.linux_distribution() linux 的版本号
4. platform.popen() 相当于 os.popen()

```
# coding=utf-8

import platform

print platform.system()
print platform.version()
print platform.release()
print platform.dist()
print platform.uname()
print platform.node()
print platform.platform()
print platform.machine()
print platform.processor()
print platform.architecture()
print platform._sys_version()
print platform.java_ver()
print platform.python_version()
print platform.python_implementation()
print platform.python_version_tuple()
print platform.python_branch()
print platform.python_compiler()
print platform.python_build()
print platform.win32_ver()
print platform.mac_ver()
print platform.linux_distribution()

print platform.popen('ifconfig','w')

```


结果

```
Linux
#76~14.04.1-Ubuntu SMP Fri Aug 12 11:47:02 UTC 2016
3.19.0-68-generic
('Ubuntu', '14.04', 'trusty')
('Linux', 'windard', '3.19.0-68-generic', '#76~14.04.1-Ubuntu SMP Fri Aug 12 11:47:02 UTC 2016', 'i686', 'i686')
windard
Linux-3.19.0-68-generic-i686-with-Ubuntu-14.04-trusty
i686
i686
('32bit', 'ELF')
('CPython', '2.7.6', '', '', 'default', 'Jun 22 2015 18:00:18', 'GCC 4.8.2')
('', '', ('', '', ''), ('', '', ''))
2.7.6
CPython
('2', '7', '6')

GCC 4.8.2
('default', 'Jun 22 2015 18:00:18')
('', '', '', '')
('', ('', '', ''), '')
('Ubuntu', '14.04', 'trusty')
<open file 'ifconfig', mode 'w' at 0xb65ebc80>lo        Link encap:本地环回
          inet 地址:127.0.0.1  掩码:255.0.0.0
          inet6 地址: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  跃点数:1
          接收数据包:50116 错误:0 丢弃:0 过载:0 帧数:0
          发送数据包:50116 错误:0 丢弃:0 过载:0 载波:0
          碰撞:0 发送队列长度:0
          接收字节:23273759 (23.2 MB)  发送字节:23273759 (23.2 MB)

wlan0     Link encap:以太网  硬件地址 9c:ad:97:d5:4d:df
          inet 地址:10.177.131.79  广播:10.177.255.255  掩码:255.255.0.0
          inet6 地址: fe80::9ead:97ff:fed5:4ddf/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  跃点数:1
          接收数据包:2197234 错误:0 丢弃:0 过载:0 帧数:573499
          发送数据包:70448 错误:0 丢弃:0 过载:0 载波:0
          碰撞:0 发送队列长度:1000
          接收字节:211655684 (211.6 MB)  发送字节:7795194 (7.7 MB)
          中断:18

```
