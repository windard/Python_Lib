#coding=utf-8

from operator import add
from time import ctime

print ctime()
for i in range(10000000):
	add(i,0)
print ctime()

print ctime()
for i in range(10000000):
	i + 0
print ctime()
