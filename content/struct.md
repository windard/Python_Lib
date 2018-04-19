## struct

python 结构化函数库，和其他的序列化函数库 json, pickle 类似。


### json 和 pickle

```
# coding=utf-8


import json
import pickle


def pickle_test():
    data = {
        'name': 'json',
        'profile': 'better'
    }
    pickle_data = pickle.dumps(data)
    print pickle_data
    print pickle.loads(pickle_data)


def json_test():
    data = {
        'name': 'pickle',
        'profile': 'worser'
    }
    json_data = json.dumps(data)
    print json_data
    print json.loads(json_data)


if __name__ == '__main__':
    pickle_test()
    json_test()

```


### struct

- struct.pack 将一个或多个数字，转化为结构化的字符串
- struct.unpack 将结构化的字符串，转化为一个或多个的数字

比如 ip 地址的转换

IPv4 的 ip 地址由四位0-255的数字组成，即由32个比特位，4个字节构成，ip 地址的数字形式即是 32 位的大整数的值。

先来将 32 位的大整数转化为四位的字节，如果直接转换的话，需要转化为比特串分段截取转换，或者将大整数位移取值

```
# -*- coding: utf-8 -*-


def bigint2byte_split(a):
    a = '{:032b}'.format(a)
    return chr(int(a[:8], 2)) + \
           chr(int(a[8:16], 2)) + \
           chr(int(a[16:24], 2)) + \
           chr(int(a[24:], 2))


def bigint2byte_shift(a):
    return chr((a & 0xff000000) >> 24) + \
           chr((a & 0xff0000) >> 16) + \
           chr((a & 0xff00) >> 8) + \
           chr((a & 0xff))


if __name__ == '__main__':
    print repr(bigint2byte_split(1324224242))
    print repr(bigint2byte_shift(1324224242))

```

这样就比较麻烦才能得到想要的结果，如果使用 struct 即可直接转换得到

```
>>> import struct
>>> struct.pack('I', 1324224242)
'\xf2\x0e\xeeN'
>>> struct.pack('>I', 1324224242)
'N\xee\x0e\xf2'
```

- `>` 表示字节序为大端序，即网络序
- `!` 表示字节序为网络序，即大端序
- `<` 表示字节序为小端序
- `I` 表示4字节无符号数
- `H` 表示2字节无符号数
- `B` 表示1字节无符号数

然后是 unpack

```
>>> struct.unpack('>IH', '\xf0\xf0\xf0\xf0\x80\x80')
(4042322160, 32896)
>>> struct.unpack('>I', 'N\xee\x0e\xf2')
(1324224242,)
```

### struct 类型表

|Format | C Type  |Python type| Standard size |
|-------|---------|-----------|---------------|
|x  | pad byte |   no value  |                |
|c  | char  |  string of length 1 | 1         |
|b  | signed char |integer |1                 |
|B  | unsigned char |  integer |1   |
|?  | _Bool |  bool  |  1   |
|h  | short  | integer |2   |
|H  | unsigned short | integer |2   |
|i  | int |integer |4   |
|I  | unsigned int |   integer| 4   |
|l  | long   | integer| 4   |
|L  | unsigned long   |integer| 4   |
|q  | long long  | integer| 8   |
|Q  | unsigned long long | integer |8   |
|f  | float  | float   |4   |
|d  | double | float  | 8   |
|s  | char[] | string  |1|
|p  | char[] | string|   |
|P  | void * | integer|    |

### 打包数据

```
# -*- coding: utf-8 -*-

import struct
from collections import namedtuple

User = namedtuple('User', ['name', 'phone', 'age'])


def pack():
    user = User(name='windard', phone='186-0757-1914', age=20)

    raw_data = struct.pack('7s13sI', user.name, user.phone, user.age)

    with open('raw_data.bin', 'wb') as f:
        f.write(raw_data)

    print repr(raw_data)


def unpack():
    with open('raw_data.bin', 'rb') as f:
        raw_data = f.read()
    data = struct.unpack('7s13sI', raw_data)
    user = User(*data)

    print user


if __name__ == '__main__':
    pack()
    unpack()

```

数据长度，默认四字节对齐，如果指定字节序，则按照原字节数.

> 字节对齐表示在有`unsigned int`的时候，如果其出现在字符串后面，则字符串需要按照四字节对齐，如果字符串在其后面，则无需对齐。

```
struct.calcsize('7s12sI')   # 24
struct.calcsize('!7s12sI')  # 23
struct.calcsize('I7s12s')   # 23
```

### 打包不定长数据

#### 计算长度

```
s = bytes(s, 'utf-8')    # Or other appropriate encoding
struct.pack("I%ds" % (len(s),), len(s), s)
```

#### 直接连接

```
struct.pack("I", len(s)) + s
```

#### 解包数据

```
int_size = struct.calcsize("I")
(i,), data = struct.unpack("I", data[:int_size]), data[int_size:]
data_content = data[i:]
```

#### 使用示例


```
# -*- coding: utf-8 -*-

import sys
import struct

if sys.version_info.major == 3:
    unicode = str


def pack_with_len(s):
    if type(s) != bytes:
        s = s.encode('utf-8')
    return struct.pack('I%ds' % len(s), len(s), s)


def pack_without_len(s):
    if type(s) != bytes:
        s = s.encode('utf-8')
    return struct.pack('I', len(s)) + s


def unpack_string(data):
    int_size = struct.calcsize("I")
    (i, ), data = struct.unpack("I", data[:int_size]), data[int_size:]
    return data


if __name__ == '__main__':
    d1 = pack_with_len('this is a very long string')
    d2 = pack_without_len('and we do know it length')
    print repr(d1)
    print repr(d2)
    print unpack_string(d1)
    print unpack_string(d2)

```
