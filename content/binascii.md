##binacsii

在上面的进制转换里面，像字符串转化为十六机制甚至是二进制的都是只能转换单个字符。                     
```
chr(x )                 #将一个整数转换为一个ASCII字符  
unichr(x )              #将一个整数转换为Unicode字符  
ord(x )                 #将一个ASCII字符转换为它的整数值  
hex(x )                 #将一个整数转换为一个十六进制字符串  
oct(x )                 #将一个整数转换为一个八进制字符串  
bin(x )                 #将一个整数转化为一个二进制字符串
```
比如说，将字符`a`的十进制，十六进制，八进制，和二进制表示出来需要这样。          
```
>>> ord('a')
97
>>> hex(ord('a'))
'0x61'
>>> oct(ord('a'))
'0141'
>>> bin(ord('a'))
'0b1100001'
```
可是如果有时候我们需要将字符串转化为十六进制数的时候，就需要binascii库了。            
其实还有一种方法的，就是字符串的内置函数encode和decode()，很强大，不做演示了。
```python
>>> import binascii
>>> a = 'I love China'
>>> binascii.b2a_hex(a)
'49206c6f7665204368696e61'
>>> binascii.hexlify(a)
'49206c6f7665204368696e61'
```
也可以将十六进制数转化为字符串。
```python
>>> import binascii
>>> a = '49206c6f7665204368696e61'
>>> binascii.a2b_hex(a)
'I love China'
>>> binascii.unhexlify(a)
'I love China'
```
甚至中文也可以转化,在我的ubuntu上当然是utf-8编码的。                  
```python
>>> import binascii
>>> binascii.b2a_hex('我爱中国')
'e68891e788b1e4b8ade59bbd'
>>> binascii.a2b_hex('e68891e788b1e4b8ade59bbd')
'\xe6\x88\x91\xe7\x88\xb1\xe4\xb8\xad\xe5\x9b\xbd'
>>> print binascii.a2b_hex('e68891e788b1e4b8ade59bbd')
我爱中国
>>> binascii.a2b_hex('e68891e788b1e4b8ade59bbd').decode('utf-8')
u'\u6211\u7231\u4e2d\u56fd'
>>> print binascii.a2b_hex('e68891e788b1e4b8ade59bbd').decode('utf-8')
我爱中国
>>> binascii.a2b_hex('e68891e788b1e4b8ade59bbd').decode('utf-8').encode('gbk')
'\xce\xd2\xb0\xae\xd6\xd0\xb9\xfa'
```
下面是我在我的windows 10下的,所以编码格式就是gbk,但是可以看到两者的unicode编码是一致的。                                       
```
>>> import binascii
>>> binascii.b2a_hex('我爱中国')
'ced2b0aed6d0b9fa'
>>> binascii.a2b_hex('ced2b0aed6d0b9fa')
'\xce\xd2\xb0\xae\xd6\xd0\xb9\xfa'
>>> binascii.a2b_hex('ced2b0aed6d0b9fa').decode('gbk')
u'\u6211\u7231\u4e2d\u56fd'
>>> print binascii.a2b_hex('ced2b0aed6d0b9fa')
我爱中国
>>> print binascii.a2b_hex('ced2b0aed6d0b9fa').decode('gbk')
我爱中国
>>> binascii.a2b_hex('ced2b0aed6d0b9fa').decode('gbk').encode('utf-8')
'\xe6\x88\x91\xe7\x88\xb1\xe4\xb8\xad\xe5\x9b\xbd'
```
接下来是binascii所有的函数列表。             
```python
binascii.a2b_uu(string)
binascii.b2a_uu(data)
binascii.a2b_base64(string)
binascii.b2a_base64(data)
binascii.a2b_qp(string[, header])
binascii.b2a_qp(data[, quotetabs, istext, header])
binascii.a2b_hqx(string)
binascii.rledecode_hqx(data)
binascii.rlecode_hqx(data)
binascii.b2a_hqx(data)
binascii.crc_hqx(data, crc)
binascii.crc32(data[, crc])
binascii.b2a_hex(data)
binascii.b2a_hex(data)
binascii.hexlify(data)
binascii.a2b_hex(hexstr)
binascii.unhexlify(hexstr)
```
