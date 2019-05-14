## uncompyle6

反编译 pyc 文件为 py 文件。

类似的还有 `uncompyle2` ，顾名思义，只能反编译 python 2 版本的 pyc 文件，而 `uncompyle6` 则是 python 2 和 python 3 通用的

```
# coding=utf-8

import uncompyle6

with open("test.py", "w") as f:
    print uncompyle6.uncompyle_file("test.pyc", f)

```

或者使用命令行

```
$ uncompyle2 -o test.py test.pyc
# 2019.05.15 00:01:29 CST
+++ okay decompyling test.pyc
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2019.05.15 00:01:29 CST
```
