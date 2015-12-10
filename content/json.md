##json

python这么强大的语言当然也可以用来处理json，两个主要的函数是`json.dumps()`和`json.loads()`分别用来将dist字典格式的Python数据编码为json数据格式，和将json数据格式解码为Python的数据格式。     
```python
import json

data = {
    'name' : 'ACME',
    'shares' : 100,
    'price' : 542.23,
    'others': ["first thing","second thing","third thing"]
}

json_str = json.dumps(data)
print json_str

python_str = json.loads(json_str)
print python_str
print python_str["name"]
print python_str["price"]
print python_str["others"][0]
```
保存为json_demo.py，运行，看一下结果。    
![json_demo.jpg](images/json_demo.jpg)
可以看到第一行是json数据格式，第二行是Python的dist数据格式，也就可以正常的读写。    
在将json数据格式转化为Python的数据格式了之后，为了更好的展示，可以使用`pprint`来代替原生的`print`，它会按照key的字幕顺序以一种更加美观的方式输出。   
```python
import json
from pprint import pprint

data = {
    'name' : 'ACME',
    'shares' : 100,
    'price' : 542.23,
    'others': ["first thing","second thing","third thing"]
}

json_str = json.dumps(data)

python_str = json.loads(json_str)
pprint(python_str)
```
保存为json_demo_2.py,运行，看一下结果。     
![json_demo_2.jpg](images/json_demo_2.jpg)     
我们还可以将json数据解析成一个Python对象。    
```python
import json

class JSONObject:
	def __init__(self,d):
		self.__dict__=d

data = {
    'name' : 'ACME',
    'shares' : 100,
    'price' : 542.23,
    'others': ["first thing","second thing","third thing"]
}

json_str = json.dumps(data)

python_str = json.loads(json_str, object_hook=JSONObject)
print isinstance(python_str,object)
print python_str.name
print python_str.price
print python_str.others[1]
```
保存为json_object.py，运行，看一下结果。     
![json_object.jpg](images/json_object.jpg)    
在解码json的时候可以采用`pprint`来获得一个比较漂亮的输出，在编码json的时候也可以在`dumps()`函数里加上参数`indent=X`来缩进从而获得一个比较漂亮的输出。     
