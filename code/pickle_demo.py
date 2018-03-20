# coding=utf-8

import pickle

# 字典也是对象
dict_data = {'country':'China',
			 'year': 68,
			 'province':['Guangzhou', 'Shanghai', 'Beijing', 'Shenzhen'],
			 'university':{
			 		'name': 'Xidian university',
			 		'location': 'Shannxi',
			 		'num': 30000
			}}

class Student(object):
	"""docstring for Student"""
	def __init__(self, name, year):
		self.name = name
		self.year = year

	def say(self):
		print "My name is {0} and I'm {1} years old".format(self.name, self.year)

Mary = Student('Mary', 21)
Mary.say()


# 存储到文件
with open('Mary_data.pkl', 'wb') as f:
	pickle.dump(Mary, f)
	
# 存储到字符串
pkl_data = pickle.dumps(dict_data)

# 看一下序列化的数据，并不美观
# print pkl_data

# 读取文件
with open('Mary_data.pkl', 'rb') as f:
	Mary_load = pickle.load(f)

print Mary_load
Mary_load.say()

# 读取字符串
dict_load = pickle.loads(pkl_data)

import pprint
pprint.pprint(dict_data) 
