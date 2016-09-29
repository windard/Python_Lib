# coding=utf-8

import cStringIO

# 不报错
s = cStringIO.StringIO()

# 报错
# s = cStringIO.StringIO("Start")

s.write("This will make exception")
