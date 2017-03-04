## glob

这个库也非常的简单，功能就是windows下的`find`或者是linux下的`grep`。           
有两个函数，`glob()`和`iglob()`,功能是一样的，只不过返回值不一样，前者返回列表，后者返回一个生成器。他们都支持绝对路径和相对路径，支持通配符。

```
#coding=utf-8

import glob

#得到当前目录下的所有python文件，返回一个列表
f = glob.glob(r'./*.py')
for i in f:
	print i

#得到父级目录下所有的文件，返回一个生成器，也能够用for循环遍历

t = glob.iglob(r'../*')

print t.next()

for j in t:
	print j

```

支持 `*`, `?`, `[]` 这三种通配符,分别表示 `0个或多个字符`,`1个或多个字符`,`指定范围内的字符`。

