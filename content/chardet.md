## chardet

识别字符串编码类型，还能返回识别的准确率

```
# coding=utf-8

import chardet

source = u'中国'
utf8_source = source.encode('utf-8')
gbk_source = source.encode('gbk')

print chardet.detect(utf8_source)
print chardet.detect(gbk_source)

```