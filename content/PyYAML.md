## PyYAML

YAML 是一种更人性化的数据序列化标准，类似于 json 或者 XML ，但是可读性更好，语法简单.

YAML 的全称是 `YAML Ain't Markup Language` 即 YAML 不是XML，具体详情可见 [YAML 官网](http://www.yaml.org/)

一个标准的 YAML 内容类似于以下结构

```
name: John Smith
age: 37
spouse:
    name: Jane Smith
    age: 25
children:
    -   name: Jimmy Smith
        age: 15
    -   name: Jenny Smith
        age: 12
```

### 读取

那我们来试一下用 Python 读取这份 YAML 文件。

```
# coding=utf-8

import yaml

with open('yaml_test.yaml', 'r') as f:
	x = yaml.load(f) 
	print x

x = yaml.load(file('yaml_test.yaml'))

print x['name']
print x['spouse']

print x['children'][0]
print x['children'][1]['age']
```

结果是这样的

```
C:\Users\dell\.ssh\Python_Lib\code (master)
λ python yaml_demo.py
{'age': 37, 'spouse': {'age': 25, 'name': 'Jane Smith'}, 'name': 'John Smith', 'children': [{'age': 15, 'name': 'Jimmy Smith'}, {'age': 12, 'name': 'Jenny Smith'}]}
John Smith
{'age': 25, 'name': 'Jane Smith'}
{'age': 15, 'name': 'Jimmy Smith'}
12
```

或者 YAML 也能这样写

```
name: Server
host:
    ip00:
        192.168.1.1
    ip01:
        one: 192.168.1.2
        two: 192.168.1.254
soft:
    apache: 2.2
    mysql: 5.2
    php:   5.3
```

读取出来的结果就是

```
{'host': {'ip01': {'two': '192.168.1.254', 'one': '192.168.1.2'}, 'ip00': '192.168.1.1'}, 'soft': {'apache': 2.2, 'php': 5.3, 'mysql': 5.2}, 'name': 'Server'}
```

### 写入

```
# coding=utf-8

import yaml

x = {'host': {'ip01': {'two': '192.168.1.254', 'one': '192.168.1.2'}, 'ip00': '192.168.1.1'}, 'soft': {'apache': 2.2, 'php': 5.3, 'mysql': 5.2}, 'name': 'Server'}
f = open("yaml_dump.yaml", "w")

yaml.dump(x, f)

f.close()
```

不知为何， 导出的效果不太理想。

```
host:
  ip00: 192.168.1.1
  ip01: {one: 192.168.1.2, two: 192.168.1.254}
name: Server
soft: {apache: 2.2, mysql: 5.2, php: 5.3}

```
