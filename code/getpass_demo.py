#coding=utf-8

import getpass

#输入不回显，默认会提示password
pass1 = getpass.getpass()
#输入不回显，但是提示 请输入密码
pass2 = getpass.getpass("请输入密码:")

print pass1
print pass2

#登录系统的用户名
print getpass.getuser()
