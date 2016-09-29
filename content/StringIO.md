## StringIO

内存文件，它的使用与正常的文件对象一致，只不过它是在内存中。

```
# coding=utf-8

import StringIO

s = StringIO.StringIO()
# s = StringIO.StringIO("Start")

s.write("This is for test!")
s.write("The last line need a line break \n")
s.write("Just like this \n")

# 回到文件开头
s.seek(0)
print s.read(),

# 最后4个字节，第二个参数表示从末尾开始读起
s.seek(-4,2)
print s.read(),

# 当前位置的前四个字节，第二个参数表示从当前位置开始读起
s.seek(-4,1)
print s.read(),

# 从第二个字节开始，读六个字节
s.seek(2)
print s.read(6)

# 文件指针当前位置
print s.pos

# 获得全部内容也可以这样
print s.getvalue(),

# 内容长度
print s.len

# 刷新缓存
s.flush()

# 读取下一行
print s.readline(),

```

```
This is for test!The last line need a line break
Just like this
is
is
is is
8
This is for test!The last line need a line break
Just like this
66
for test!The last line need a line break
```

## cStringIO

在 Python 中，除了有 StringIO 之外，还有 cStringIO，用法与 StringIO 基本一致，但是运行效率更高。不过有两个需要注意的地方。

1. cStringIO.StringIO不能作为基类被继承；
2. 创建cStringIO.StringIO对象时，如果初始化函数提供了初始化数据，新生成的对象是只读的。

``` python
# coding=utf-8

import cStringIO

# 不报错
s = cStringIO.StringIO()

# 报错
# s = cStringIO.StringIO("Start")

s.write("This will make exception")

```

## BytesIO

StringIO 操作的是 str ， 是字节，但是如果想要操作二进制数据，就需要使用 BytesIO，来操作比特，bytes。

```
# coding=utf-8

from io import BytesIO

f = BytesIO()

f.write("This is test")
print f.getvalue()

```
