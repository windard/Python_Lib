#coding=utf-8
import random

#生成一个0到1之间的随机数
print random.random()

#生成一个a与b之间的随机符号数
print random.uniform(10,50)
print random.uniform(50,10)

#生成一个大于a小于b的随机整数
print random.randint(10,50)

#生成一个指定范围内按基数递增的集合中的一个随机元素
print random.randrange(10,50,10)
#上一句相当于这一句
print random.choice(range(10,50,10))

#从指定序列中随机选取一个元素
print random.choice("hello,world")
print random.choice(['hello','world'])
print random.choice(('hello','world',"hehe"))

#将一个列表中的序列打乱,返回原来的数组
p = ['1','2','3','four','FIVE','6']
random.shuffle(p)
print p

#生成一个指定序列中指定长度的片段
p = ['1','2','3','four','FIVE','6']
print random.sample(p,3)