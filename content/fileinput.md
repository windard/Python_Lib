## fileinput

这是一个文件操作的库，主要有以下的几个函数


```
    close()
        Close the sequence.

    filelineno()
        Return the line number in the current file. Before the first line
        has been read, returns 0. After the last line of the last file has
        been read, returns the line number of that line within the file.

    filename()
        Return the name of the file currently being read.
        Before the first line has been read, returns None.

    input(files=None, inplace=0, backup='', bufsize=0, mode='r', openhook=None)
        Return an instance of the FileInput class, which can be iterated.

        The parameters are passed to the constructor of the FileInput class.
        The returned instance, in addition to being an iterator,
        keeps global state for the functions of this module,.

    isfirstline()
        Returns true the line just read is the first line of its file,
        otherwise returns false.

    isstdin()
        Returns true if the last line was read from sys.stdin,
        otherwise returns false.

    lineno()
        Return the cumulative line number of the line that has just been read.
        Before the first line has been read, returns 0. After the last line
        of the last file has been read, returns the line number of that line.

    nextfile()
        Close the current file so that the next iteration will read the first
        line from the next file (if any); lines not read from the file will
        not count towards the cumulative line count. The filename is not
        changed until after the first line of the next file has been read.
        Before the first line has been read, this function has no effect;
        it cannot be used to skip the first file. After the last line of the
        last file has been read, this function has no effect.
```

其功能分别为

- `input(files=None, inplace=0, backup='', bufsize=0, mode='r', openhook=None) ` 输入文件或多个文件
	- `inplace=True` 表示原地处理，即输入文件与脚本文件一致
	- `backup` 备份文件
	- `bufsize` 一次读取的大小
	- `mode` 打开文件格式
	- `openhook` 打开文件钩子
- `filename` 返回当前处理的文件名
- `lineno` 返回当前行的行数，行数是所有文件累计的
- `filelineno` 返回当前文件的行数
- `isfirstline` 当时处理的是否是当前文件的第一行
- `isstdin` 当前是否处理的是 为 sys.stdin 屏幕输入流
- `nextfile` 关闭当前文件，跳到下一个文件，跳过的行数不计
- `close` 关闭整个文件链，迭代结束


一个典型应用，给 Python 脚本添加行号

```
# coding=utf-8

import fileinput

for line in fileinput.input(inplace=True):
    line = line.rstrip()
    num = fileinput.lineno()
    print '%-50s# %2i' % (line, num)

```

然后对自己执行

```
python fileinput_demo.py fileinput_demo.py
```

```
# coding=utf-8                                    #  1
                                                  #  2
import fileinput                                  #  3
                                                  #  4
for line in fileinput.input(inplace=True):        #  5
    line = line.rstrip()                          #  6
    num = fileinput.lineno()                      #  7
    print '%-50s# %2i' % (line, num)              #  8

```