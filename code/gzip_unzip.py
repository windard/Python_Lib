#coding=utf-8

import gzip

g = gzip.open('zipfile_demo.gz','rb')
f = open('zipfile_demo.py','rb')
f.write(g.read())
f.close()
g.close()
