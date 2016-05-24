## termcolor

在终端中改变颜色的库，除了 colorama 之外，常用的就是 termcolor 了，它的颜色值也比前者多一些。

```python
#coding=utf-8

import sys
from termcolor import colored, cprint

text = colored('Hello, World!', 'red', attrs=['reverse', 'blink'])
print(text)
cprint('Hello, World!', 'green', 'on_red')

print_red_on_cyan = lambda x: cprint(x, 'red', 'on_cyan')
print_red_on_cyan('Hello, World!')
print_red_on_cyan('Hello, Universe!')

for i in range(10):
    cprint(i, 'magenta', end=' ')

cprint("Attention!", 'red', attrs=['bold'], file=sys.stderr)
```

![color_linux](images/color_linux.png)

它的颜色值有

```
>>> termcolor.ATTRIBUTES
{'bold': 1, 'blink': 5, 'dark': 2, 'concealed': 8, 'underline': 4, 'reverse': 7}
>>> termcolor.COLORS
{'blue': 34, 'grey': 30, 'yellow': 33, 'green': 32, 'cyan': 36, 'magenta': 35, 'white': 37, 'red': 31}
>>> termcolor.HIGHLIGHTS
{'on_cyan': 46, 'on_white': 47, 'on_grey': 40, 'on_yellow': 43, 'on_blue': 44, 'on_magenta': 45, 'on_red': 41, 'on_green': 42}
>>> termcolor.RESET
'\x1b[0m'

```
