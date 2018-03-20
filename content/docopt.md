## docopt

这是一个比 argparse 更好用的命令行参数解释器，可以将很多复杂的命令行参数直接解析。

```
# coding=utf-8

"""Usage: arguments_example.py [-vqrh] [FILE] ...
          arguments_example.py (--left | --right) CORRECTION FILE
Process FILE and optionally apply correction to either left-hand side or
right-hand side.
Arguments:
  FILE        optional input file
  CORRECTION  correction angle, needs FILE, --left or --right to be present
Options:
  -h --help
  -v       verbose mode
  -q       quiet mode
  -r       make report
  --left   use left-hand side
  --right  use right-hand side
"""
from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    print arguments['FILE']
    print arguments['--left']
    print arguments['--right']
```

参考

[docopt/docopt](https://github.com/docopt/docopt)

[docopt - 创建漂亮的命令行交互界面](https://wp-lai.gitbooks.io/learn-python/content/0MOOC/docopt.html)

[docopt：为Python程序创造一个优雅的命令行界面](http://hao.jobbole.com/docopt/)

[docopt——好用的Python命令行参数解释器](https://xuanwo.org/2016/04/04/docopt-intro/)