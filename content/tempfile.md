## tempfile

用来生成临时文件的库，常用的有 `tempfile.TemporaryFile`, 可以安全的创建临时文件，实际并未创建文件，只在内存中，关闭之后就会被释放。

还有 `tempfile.mkstemp` 可以手动创建一个真实的临时文件用来使用, 函数返回一个文件路径。

```
# -*- coding: utf-8 -*-
import tempfile

# create temp file
print(tempfile.mktemp())

# create a temporary file and write some data to it
fp = tempfile.TemporaryFile()
fp.write(b'Hello world!')
# read data from file
fp.seek(0)
print(fp.read())
# close the file, it will be removed
fp.close()

# create a temporary file using a context manager
with tempfile.TemporaryFile() as fp:
    fp.write(b'Hello world!')
    fp.seek(0)
    print(fp.read())

# file is now closed and removed

# python 3
# create a temporary directory using the context manager
# with tempfile.TemporaryDirectory() as tmpdirname:
#     print('created temporary directory', tmpdirname)
# directory and contents have been removed


```
