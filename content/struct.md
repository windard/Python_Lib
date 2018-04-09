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

## struct 类型表

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
