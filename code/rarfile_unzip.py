#coding=utf-8

import rarfile

g = rarfile.RarFile('demo.rar')

#解压到当前文件夹
g.extractall()

g.close()
