## pickle

pickle 数据持久化存储，实现 Python 数据的序列化和反序列话。

第一次见到 pickle 是在 《head first Python》 当时就对这种行为很不能理解，序列化和反序列化有什么用么？后来了解学习到了 json 数据结构，知道很多数据在不同的编程语言或者环境下是有不同的书写格式，为了统一保存传输，就需要对数据进行不同格式的编码。

pickle 只有四个主要函数，功能就是将程序中的对象进行序列化保存到文件中去，或者将对象从文件中反序列话出来。

```
dump(object, file)
dumps(object) -> string
load(file) -> object
loads(string) -> object
```

```
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

```

输出

```
λ python pickle_demo.py
My name is Mary and I'm 21 years old
<__main__.Student object at 0x02E3DD90>
My name is Mary and I'm 21 years old
{'country': 'China',
 'province': ['Guangzhou', 'Shanghai', 'Beijing', 'Shenzhen'],
 'university': {'location': 'Shannxi',
                'name': 'Xidian university',
                'num': 30000},
 'year': 68}
```

### 重点

pickle 与 json 的区别，json 的 dumps 和 loads 的返回都是字典，而 pickle 可以是对象，将对象 dumps 然后 loads 出来。

pickle 返回的对象是 完全的重现传入的对象，不仅仅是构造参数，类属性和实例属性。还有私有变量和挂载的的变量方法。
