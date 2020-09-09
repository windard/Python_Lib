## json

python这么强大的语言当然也可以用来处理json，两个主要的函数是`json.dumps()`和`json.loads()`分别用来将dist字典格式的Python数据编码为json数据格式字符串，和将json数据格式字符串解码为Python的数据格式。

> 还有 ujson 更快，simplejson 兼容性更强

分别有四个主要的函数

```
# 将 python 的数据格式转换为 json 字符串并存储到文件中
dump(obj, fp, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, encoding='utf-8', default=None, sort_keys=False, **kw) 
# 将 python 的数据格式转换为 json 字符串
dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, encoding='utf-8', default=None, sort_keys=False, **kw) 
# 从文件中读取 json 字符串并转换为python 的数据格式
load(fp, encoding=None, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None, **kw) 
# 将 json 字符串转换为 python 的数据格式
loads(s, encoding=None, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None, **kw) 
```

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

### 2016-01-13 更新

在 Python 中 eval 和 str(unicode) 的功能也可以做 json 数据格式的转化

```
>>> data = {
...     'name' : 'ACME',
...     'shares' : 100,
...     'price' : 542.23,
...     'others': ["first thing","second thing","third thing"]
... }
>>> json_str = str(data)
>>> json_str
"{'price': 542.23, 'name': 'ACME', 'shares': 100, 'others': ['first thing', 'second thing', 'third thing']}"
>>> eval(json_str)
{'price': 542.23, 'name': 'ACME', 'shares': 100, 'others': ['first thing', 'second thing', 'third thing']}
```

但是有一个问题，正确在 json 中为 true，但是在 Python 中为 True，失败在 json 中为 false ，但是在 Python 是为 False。

```
>>> data = "{'name':'ACMA','status':false}"
>>> eval(data)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<string>", line 1, in <module>
NameError: name 'false' is not defined
```

对于 json 数据格式的操作还是让专业的库来干吧。

### 2017-03-18 更新

json 格式数据与 Python 中的 字典(dict) 并不完全一致，json 只能是双引号包围的字符串，而 Python 中的字符串可以用双引号也可以用单引号。

```
+-------------------+---------------+
| Python            | JSON          |
+===================+===============+
| dict              | object        |
+-------------------+---------------+
| list, tuple       | array         |
+-------------------+---------------+
| str, unicode      | string        |
+-------------------+---------------+
| int, long, float  | number        |
+-------------------+---------------+
| True              | true          |
+-------------------+---------------+
| False             | false         |
+-------------------+---------------+
| None              | null          |
+-------------------+---------------+
```

```
JSONEncoder().encode({"foo": ["bar", "baz"]}) # 将字典格式转换为 json 字符串
JSONDecoder().decode('{"foo": ["bar", "baz"]}') # 将 json 字符串转换为字典格式
```

### 2017-10-22 更新

json 和 dict 还有两个地方不一样
- dict 在所有的键值对之后还可以有逗号，json 在所有的键值对最后没有逗号
- dict 的键可以是数字，json 的键不能是数字，只能是字符串

### 2018-06-21

- `json.dumps(obj, indent=4)` 能够输出一个格式化的字符串，有换行有缩进。
- `json.dumps(obj, separators=(',',':'))` 能够对输出字符串进行一个简单的压缩，取消空格.因为默认是 `(', ', ': ')`
- `json.dumps(obj, ensure_ascii=False)` 能够输出 utf-8 格式的中文即可见的中文，而非 Unicode 格式的中文 `\uXXXX`

### 2020-09-09

正常的 json 字符串像这样 `'{"price": 542.23, "name": "ACME", "shares": 100, "others": ["first thing", "second thing", "third thing"]}'` 都是没问题的，但是如果在 json 对象中，key 或者 value 里存在控制字符，就会出现 `Invalid Control Character` 的 `ValueError`。

**什么是控制字符？**  
ACSII 码表，排名前三十二位和最后一位的字符就是控制字符，包括 `\t`, `\n`, `\r` 等。

[ASCII码一览表](http://c.biancheng.net/c/ascii/)

**出现控制字符怎么办？**  

比如这样的 json 字符串 `'{"price": 542.23, "name": "ACME", "sh\rares": 100, "others": ["first thing", "second\t thing", "third\n thing"]}'`

不要惊慌，在解析的时候，传入参数 `strict=False` 即可。

```
In [28]: s = '{"price": 542.23, "name": "ACME", "shares": 100, "others": ["first thing", "second thing", "third thing"]}'

In [29]: json.loads(s)
Out[29]:
{u'name': u'ACME',
 u'others': [u'first thing', u'second thing', u'third thing'],
 u'price': 542.23,
 u'shares': 100}

In [30]: s = '{"price": 542.23, "name": "ACME", "sh\rares": 100, "others": ["first thing", "second\t thing", "third\n thing"]}'

In [31]: json.loads(s)
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-31-48280973ea66> in <module>()
----> 1 json.loads(s)

/Users/bytedance/miniconda/envs/byted/lib/python2.7/json/__init__.pyc in loads(s, encoding, cls, object_hook, parse_float, parse_int, parse_constant, object_pairs_hook, **kw)
    337             parse_int is None and parse_float is None and
    338             parse_constant is None and object_pairs_hook is None and not kw):
--> 339         return _default_decoder.decode(s)
    340     if cls is None:
    341         cls = JSONDecoder

/Users/bytedance/miniconda/envs/byted/lib/python2.7/json/decoder.pyc in decode(self, s, _w)
    362
    363         """
--> 364         obj, end = self.raw_decode(s, idx=_w(s, 0).end())
    365         end = _w(s, end).end()
    366         if end != len(s):

/Users/bytedance/miniconda/envs/byted/lib/python2.7/json/decoder.pyc in raw_decode(self, s, idx)
    378         """
    379         try:
--> 380             obj, end = self.scan_once(s, idx)
    381         except StopIteration:
    382             raise ValueError("No JSON object could be decoded")

ValueError: Invalid control character at: line 1 column 38 (char 37)

In [32]: json.loads(s, strict=False)
Out[32]:
{u'name': u'ACME',
 u'others': [u'first thing', u'second\t thing', u'third\n thing'],
 u'price': 542.23,
 u'sh\rares': 100}
```

**还需要注意两点**  
1. 如果不是在 json 字符串的字符串类型中有控制字符，是可以正常解析的，在 json 的两个 key 之间是可以有正常的换行符，比如这样的字符串 `'\n{"price": 542.23,\n "name": "ACME", \t"shares": 100, "others": ["first thing", "second thing",\n "third thing"]}'`
2. 如果不是手动换行符，而是出现了换行，也是一样的换行符，主要是在 json 的每个元素里，不能有换行符。

```
In [34]: s = '\n{"price": 542.23,\n "name": "ACME", \t"shares": 100, "others": ["first thing", "second thing",\n "third thing"]}'

In [35]: json.loads(s)
Out[35]:
{u'name': u'ACME',
 u'others': [u'first thing', u'second thing', u'third thing'],
 u'price': 542.23,
 u'shares': 100}

In [37]: s= """{"price": 542.23, "name": "ACME", "shares": 100, "others": ["first thing", "second
    ...: thing", "third thing"]}"""

In [38]: s
Out[38]: '{"price": 542.23, "name": "ACME", "shares": 100, "others": ["first thing", "second \nthing", "third thing"]}'

In [39]: json.loads(s)
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-39-48280973ea66> in <module>()
----> 1 json.loads(s)

/Users/bytedance/miniconda/envs/byted/lib/python2.7/json/__init__.pyc in loads(s, encoding, cls, object_hook, parse_float, parse_int, parse_constant, object_pairs_hook, **kw)
    337             parse_int is None and parse_float is None and
    338             parse_constant is None and object_pairs_hook is None and not kw):
--> 339         return _default_decoder.decode(s)
    340     if cls is None:
    341         cls = JSONDecoder

/Users/bytedance/miniconda/envs/byted/lib/python2.7/json/decoder.pyc in decode(self, s, _w)
    362
    363         """
--> 364         obj, end = self.raw_decode(s, idx=_w(s, 0).end())
    365         end = _w(s, end).end()
    366         if end != len(s):

/Users/bytedance/miniconda/envs/byted/lib/python2.7/json/decoder.pyc in raw_decode(self, s, idx)
    378         """
    379         try:
--> 380             obj, end = self.scan_once(s, idx)
    381         except StopIteration:
    382             raise ValueError("No JSON object could be decoded")

ValueError: Invalid control character at: line 1 column 84 (char 83)

```

