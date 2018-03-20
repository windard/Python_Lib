# coding=utf-8

import jieba.posseg as posg

words = posg.cut("我爱北京天安门")

for word,flag in words:
	print("%s %s"%(word, flag))