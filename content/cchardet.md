## cchardet

c 语言写的字符串编码识别库，更快更准确

```
# coding=utf-8

import cchardet

source = u'你好，世界'
utf8_source = source.encode('utf-8')
gbk_source = source.encode('gbk')

print cchardet.detect(utf8_source)
print cchardet.detect(gbk_source)

print utf8_source.decode(cchardet.detect(utf8_source)['encoding'])
print utf8_source.decode(cchardet.detect(gbk_source)['encoding'])

```