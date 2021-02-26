## yaml

yaml 和 json 是数据格式化的两种不同方式，json 更加人性化，更加易读一些，个人比较喜欢 json。

但是 yaml 功能更强大，而且 yaml 是 json 的超集，每个 json 文件都是合法的 yaml 文件，也就是说，市面上任何一个标准的 yaml 解析器，都是可以无缝兼容 json 格式的。
> every JSON file is also a valid YAML file, reference from [Relation to JSON](https://yaml.org/spec/1.2/spec.html#id2759572)

## 与 json 的差异

主要从四个方面来比较一下，解析速度，内存占用，表现力，可移植性

### 解析速度
解析速度取决于解析器的实现，一般来说，json 的使用和实现都比 yaml 要多，也就是说能够取得更好的性能。
> 虽然有人说，使用 json 就是基本无视性能了。😂

### 内存占用
一般来说，yaml 文件会比 json 文件略小一些，因为 yaml 使用换行做分隔符，而 json 中有大量的引号 `"` 和逗号 `,`, 所以 yaml 的内存效率会更高。

### 表现力
除了绝对性能之外，还要考虑一些其他的因素，比如表现力或者说易读性，可理解性。
毫无疑问，json 的语法更为简单，而 yaml 的语法复杂，还有各种极端情况和特殊场景，而且还有内部引用和注释，甚至 yaml 的语法还能兼容 json ，所以 yaml 的解释器也很复杂。

有人说 python 程序员更喜欢 yaml ，但是我不这么认为。

### 可移植性
很难想象现在还有哪门现代编程语言不支持 json，一般起码都会有一个官方的标准库实现。而 yaml 并没有那么普及，一般最多也就是只有一个官方库的实现，而且还支持部分实现，没有完全实现 yaml 的全部语法。

## 简单使用

和 json 一样，主要就是序列化和反序列化操作，不过一般因为安全性问题，不直接使用 `load` 和 `dump` 而是使用 `safe_load` 和 `safe_dump`

```python
# -*- coding: utf-8 -*-
import yaml


if __name__ == '__main__':
    data = {
        'name': 'ACME',
        'object': {'complex': True, 'description': 'complex object'},
        'shares': 100,
        'price': 542.23,
        'others': ["first thing", "second thing", "third thing"],
    }
    raw_yaml_data = yaml.safe_dump(data)
    print(raw_yaml_data)
    print(yaml.safe_load(raw_yaml_data))

```

执行结果

```
$ python yaml_demo.py
name: ACME
object:
  complex: true
  description: complex object
others:
- first thing
- second thing
- third thing
price: 542.23
shares: 100

{'price': 542.23, 'object': {'complex': True, 'description': 'complex object'}, 'name': 'ACME', 'shares': 100, 'others': ['first thing', 'second thing', 'third thing']}
```

使用 yaml 文件存取, 实际上还是同一个方法。

```python
# -*- coding: utf-8 -*-
import yaml


if __name__ == '__main__':
    data = {
        'name': 'ACME',
        'object': {'complex': True, 'description': 'complex object'},
        'shares': 100,
        'price': 542.23,
        'others': ["first thing", "second thing", "third thing"],
    }
    with open('yaml_test.yaml', 'w') as f:
        raw_yaml_data = yaml.safe_dump(data, f)

    with open('yaml_test.yaml', 'r') as f:
        print(yaml.safe_load(f))

```

## 参考链接

[13.10. json — JS 对象简谱](https://learnku.com/docs/pymotw/json-javascript-object-notation/3440)       
[YAML和JSON有什么区别？](https://my.oschina.net/u/3797416/blog/3147822)      
[YAML Ain’t Markup Language (YAML™) Version 1.2](https://yaml.org/spec/1.2/spec.html#id2759572)    
[YAML和JSON有什么区别？](https://www.codenong.com/1726802/)          
[What is the difference between YAML and JSON?](https://stackoverflow.com/questions/1726802/what-is-the-difference-between-yaml-and-json)          
