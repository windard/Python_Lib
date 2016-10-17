## unidecode

这是一个神奇的 python 库，它能够 unicode 字符转换成 ascii 字符，或许你并没有觉得什么特别，但是如果我说它能够把把汉字转换成拼音，这下你明白了把。

它的使用也非常简单，只有一个方法，输入 unicode 编码的字符，还你一个 ascii 编码的字符。

比如说

```
>>> from unidecode import unidecode
>>> unidecode(u'我爱中国')
'Wo Ai Zhong Guo '
>>> unidecode(u'魁魅魍魉')
'Kui Mei Wang Liang '
```

它是一个用来做全球化或者说标准化的库，也就是说其他的语言也可以，但是我也不会就不测试了。

这是一个可以输入标准化的函数

```
# coding=utf-8

import re
import sys
import unicodedata
from unidecode import unidecode

def slugify(value):
    if type(value) == unicode:
        value = unicode(unidecode(value))
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return  re.sub('[-\s]+', '-', value)

if __name__ == '__main__':
    print slugify(raw_input().decode(sys.stdin.encoding))
```

参考链接
[把Unicode转换为合法的文件名（ASCII）](https://blog.blahgeek.com/ba-unicodezhuan-huan-wei-he-fa-de-wen-jian-ming-ascii.html)
