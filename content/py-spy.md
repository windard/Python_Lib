## py-spy

python 性能分析工具，可以用来生成火焰图，查看程序代码性能瓶颈，或者动态查看代码运行时间消耗。

### record

生成火焰图，🔥

```
py-spy record -o profile.svg --pid 12345
# OR
py-spy record -o profile.svg -- python myprogram.py
```

### top

查看程序运行时

```
py-spy top --pid 12345
# OR
py-spy top -- python myprogram.py
```

### dump

查看函数调用堆栈

```
py-spy dump --pid 12345
```

### 火焰图

查看火焰图中占比最大的代码行数进行分析。

[如何读懂火焰图？](http://www.ruanyifeng.com/blog/2017/09/flame-graph.html)

### pyflame

pyflame 工具也可以用来生成火焰图做性能分析，就是用起来比较麻烦。
