#coding=utf-8
import sys

#默认第0个是程序自身
print sys.argv[1]

#默认传进来的参数都是字符串，所以这样的加法是直接相加
print sys.argv[2] + sys.argv[3]

#如果想要做加法的话需要这样相加
print int(sys.argv[2])+int(sys.argv[3])

#计算传进来的未知长度的数字之和
num = 0
for i in sys.argv[2:]:
	num = num+int(i)

print num
