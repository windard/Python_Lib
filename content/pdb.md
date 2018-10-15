## pdb

打断点神器，再也不用依靠 pycharm 来打断点了。

标准用法

```
import pdb
pdb.set_trace()
```

然后即可使用当前位置的变量，环境和堆栈等相关信息。

pdb 中的命令

0. help [command] 显示相关语句帮助
1. n|next 下一步，不进入函数内部
7. j|jump [lineno] 跳转至某一行
2. c|continue 继续运行,没有断点则退出 pdb 调试
3. q|exit|quit 报错退出
4. l|list 列出上下文相关代码
5. w|where 显示堆栈信息
6. b|break [lineno] 打断点
8. cl|clear 清除所有断点
9. a|args 当前环境变量
10. r|return 退出当前函数
11. whatis [arg] 查看变量类型
12. s|step 下一步，进入函数内部

还可以使用 `python -m pdb file.py` 使用 pdb 调试代码，默认停在第一行

2018-09-15

需注意两点
1. 在 pdb 中不能创建新的变量
2. 在 pdb 中不能给已有的变量赋值

2018-09-16

可以设置变量，但是 a,b,c 都被占用了，所以不能直接设置
