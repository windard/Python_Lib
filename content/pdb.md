## pdb

打断点神器，再也不用依靠 pycharm 来打断点了。

标准用法

```
import pdb
pdb.set_trace()
```

然后就可以了。

2018-09-15

需注意两点
1. 在 pdb 中不能创建新的变量
2. 在 pdb 中不能给已有的变量赋值
