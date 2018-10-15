## code

提供 python 交互执行解释器

可以使用 `code.interact()` 建立一个 交互式 shell ，或者使用 `code.InteractiveConsole` 自己构建

```
# doding=utf-8

import code

name = "windard"

# console = code.InteractiveConsole(locals())
# console.interact()

code.interact(local=locals())

```

看源代码 `interact` 的实现

```
def interact(banner=None, readfunc=None, local=None):
    """Closely emulate the interactive Python interpreter.

    This is a backwards compatible interface to the InteractiveConsole
    class.  When readfunc is not specified, it attempts to import the
    readline module to enable GNU readline if it is available.

    Arguments (all optional, all default to None):

    banner -- passed to InteractiveConsole.interact()
    readfunc -- if not None, replaces InteractiveConsole.raw_input()
    local -- passed to InteractiveInterpreter.__init__()

    """
    console = InteractiveConsole(local)
    if readfunc is not None:
        console.raw_input = readfunc
    else:
        try:
            import readline
        except ImportError:
            pass
    console.interact(banner)

```


在 code 中的交互式命令行不能改变样式，也没有自动补全，但是在默认的 python 交互式命令行中可以修改样式。


```
>>> import sys
>>> sys.ps1
'>>> '
>>> sys.ps2
'... '
>>> sys.ps1 = '--------'
--------sys.ps2 = '********'
--------def foo():
********        pass
********
```


