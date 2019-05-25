## py_compile

将 py 文件编译为 pyc 文件，在前两年还说是别人都无法反编译出源文件，但是现在连[在线反编译网站](https://tool.lu/pyc/)都有了。

源代码保护还是需要再想想别的法子. 比如使用 cython 编译成 so 链接库。

py_compile 是 python 自带的官方库，在单个 python 文件中边解释边运行，在 python 类库里引用运行的时候就会自动编译出 pyc 文件。

pyc 文件是跨平台，区分版本的。在 python 虚拟机中运行，和 Java 类似。

### 使用 

```
# coding=utf-8

import py_compile

py_compile.compile("test.py")

```

或者 在命令行中执行

```
$ python -m py_compile test.py
```

还可以使用 py_compile 编译为 `pyo` 文件，是优化后的二进制文件

```
$ python -O -m py_compile test.py
```

不过好像没差吖。。。

确实没什么差别，可以看到[现有的编译器并没有太大的优化](https://docs.pythontab.com/python/python2.7/modules.html#python)

### 高级用法

编译整个文件夹,使用 `compileall` 库

```
# coding=utf-8

import compileall

# 编译单个文件
print compileall.compile_file("test.py")

# 编译整个文件夹
print compileall.compile_dir("home")

```

1. 使用 `compileall.compile_dir` 实际上也是将文件夹中的源代码单个调用 `compileall.compile_file` 方法
2. 使用 `compileall.compile_file` 实际上也是调用 `py_compile.compile` 方法
3. 编译完成后的 pyc 文件在源目录下
4. 调用成功后会返回 `1`

```
$ python compileall_demo.py
Compiling test.py ...
1
Listing home ...
Compiling home/__init__.py ...
Compiling home/index.py ...
1
```

也可以使用命令行

```
$ python -m compileall home
Listing home ...
Compiling home/__init__.py ...
Compiling home/index.py ...
```
