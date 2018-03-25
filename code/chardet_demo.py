# coding=utf-8

import chardet

source = u'你好，世界'
utf8_source = source.encode('utf-8')
gbk_source = source.encode('gbk')

print chardet.detect(utf8_source)
print chardet.detect(gbk_source)

print utf8_source.decode(chardet.detect(utf8_source)['encoding'])
print utf8_source.decode(chardet.detect(gbk_source)['encoding'])
