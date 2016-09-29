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
