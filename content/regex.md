## regex

更加强大的 正则表达式

一个比较典型的应用就是重复匹配，re 的匹配默认只会认准最后一个。
> https://bugs.python.org/issue7132

比如说获取所有的匹配结果。

```

In [1]: import re

In [2]: re.match(r"(?P<key>\w+):(?P<value>\d+)", "haha:1").groups()
Out[2]: ('haha', '1')

In [3]: re.match(r"(?P<key>\w+):(?P<value>\d+)", "haha:1").groupdict()
Out[3]: {'key': 'haha', 'value': '1'}

In [4]: re.search(r"((?P<key>\w+):(?P<value>\d+);)*", "haha:1;laal:2;").groups()
Out[4]: ('laal:2;', 'laal', '2')

In [5]: re.search(r"((?P<key>\w+):(?P<value>\d+);)*", "haha:1;laal:2;").groupdict()
Out[5]: {'key': 'laal', 'value': '2'}

In [6]: re.search(r"(?:(?P<key>\w+):(?P<value>\d+);)*", "haha:1;laal:2;").groups()
Out[6]: ('laal', '2')

In [7]: import regex

In [8]: regex.search(r"(?:(?P<key>\w+):(?P<value>\d+);)*", "haha:1;laal:2;").groups()
Out[8]: ('laal', '2')

In [9]: regex.search(r"(?:(?P<key>\w+):(?P<value>\d+);)*", "haha:1;laal:2;").capturesdict()
Out[9]: {'key': ['haha', 'laal'], 'value': ['1', '2']}

In [10]: regex.search(r"(?:(?P<key>\w+):(?P<value>\d+);)*", "haha:1;laal:2;").captures("key")
Out[10]: ['haha', 'laal']
```

或者说，找到字符串中的所有重复子串，或者找到数组中所有的指定子串，因为 re 好像不能使用 `\g` 来判断重复 

```
In [1]: import regex

In [2]: # 找到数组里的所有数字

In [3]: regex.match(r"((?P<rep>(\d+)\3*)[a-zA-Z]*)+", "2333abc3uio890da123").capturesdict()
Out[3]: {'rep': ['2333', '3', '890', '123']}

In [2]: # 找到数组中所有的重复数字子串

In [3]: regex.match(r"((?P<rep>(\d)\3*)[a-zA-Z]*)+", "2333abc3uio890da1112233").capturesdict()
Out[3]: {'rep': ['2', '333', '3', '8', '9', '0', '111', '22', '33']}

In [4]: # 找到数组中所有的重复子串

In [5]: regex.match(r"(?P<rep>(\w)\2*)+", "aaabbcccdddd").capturesdict()
Out[5]: {'rep': ['aaa', 'bb', 'ccc', 'dddd']}

In [6]: # 使用 re 只能找到所有的连续重复子串，或者第一个重复的子串

In [8]: import re

In [9]: re.search(r"(.+?)\1+", 'dxabcabcyyyydxycxcxz').group()
Out[9]: 'abcabc'

In [9]: re.findall(r"\d+", "2333abc3uio890da123")
Out[9]: ['2333', '3', '890', '123']
```

