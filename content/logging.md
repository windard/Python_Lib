## logging

标准的输出日志库，比每次用 print 输出不知道高到哪里去了。

```python
#coding=utf-8

import logging
import sys

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}

if len(sys.argv) > 1:
    level_name = sys.argv[1]
    level = LEVELS.get(level_name, logging.NOTSET)
    logging.basicConfig(level=level)

logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical error message')

```

logging 共分五个 log 等级，默认输出的 Level 为 warning 等级，可以设定为其他等级就可以将代码中的每一个等级大于等于 Level 的问题都输出。

```python
#coding=utf-8

import sys
import logging
    
logger = logging.getLogger("Test Logging")
formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(lineno)-4d %(message)s', '%Y%b%d %a %H:%M:%S')
file_handler = logging.FileHandler("test.log")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.WARNING)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')

logger.removeHandler(stream_handler)
logger.critical('This is a critical error message')

```

设定 log 的的格式，和 log 的输出位置，可以在屏幕上，也可以输出到文件中，可以将不同地方的 log 输出等级设为不同。

关于输出的 log 格式

|格式                                    |用处                                          |
|---                                      |---                                              |
|%(name)s                         | Logger的名字                                       |
|%(levelno)s                      | 数字形式的日志级别                                       |
|%(levelname)s                 |文本形式的日志级别                                       |
|%(pathname)s                | 调用日志输出函数的模块的完整路径名，可能没有                                       |
|%(filename)s                    |调用日志输出函数的模块的文件名                                       |
|%(module)s                     | 调用日志输出函数的模块名                                      |
|%(funcName)s                 |调用日志输出函数的函数名                                     |
|%(lineno)d                        | 调用日志输出函数的语句所在的代码行                                      |
|%(created)f                       | 当前时间，用UNIX标准的表示时间的浮点数表示                                        |
|%(relativeCreated)d        | 输出日志信息时的，自Logger创建以来的毫秒数                                      |
|%(asctime)s                     | 字符串形式的当前时间。默认格式是“2003-07-08 16:49:45,896”。逗号后面的是毫秒                          |
|%(thread)d                      |   线程ID。可能没有                                      |
|%(threadName)s            |  线程名。可能没有                                      |
|%(process)d                    |  进程ID。可能没有                                        |
|%(message)s                 |  用户输出的消息                                     |

一般常用的 logging

```
import sys
import logging

logger = logging.getLogger("Socket Logging")
formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(lineno)-4d %(message)s', '%Y %b %d %a %H:%M:%S',)

file_handler = logging.FileHandler("SocketServer.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)

logger.setLevel(logging.DEBUG)
```

也可以这样配置日志

```
# coding=utf-8
import logging

def main():
    # Configure the logging system
    logging.basicConfig(
        filename='app.log',
        level=logging.ERROR,
        format='%(levelname)s:%(asctime)s:%(message)s'
    )

    # Variables (to make the calls that follow work)
    hostname = 'www.python.org'
    item = 'spam'
    filename = 'data.csv'
    mode = 'r'

    # Example logging calls (insert into your program)
    logging.critical('Host %s unknown', hostname)
    logging.error("Couldn't find %r", item)
    logging.warning('Feature is deprecated')
    logging.info('Opening file %r, mode=%r', filename, mode)
    logging.debug('Got here')

if __name__ == '__main__':
    main()
```

关于 logger 输出异常堆栈，无论使用 `logger.info` 或者 `logger.error` 输出格式都是一样的，只是日志等级不一样，但是有时在输出异常的时候，我们不只是需要知道异常名称，还需要知道异常的上下文，堆栈信息等，特别是在多线程中，子线程的异常不会被主线程捕获输出，只能通过日志打印出来。

所以可以使用 `logger.exception` 代替 `logger.error` ，日志等级也是 `error`, 但是会打印出异常的堆栈信息。

logging 如果不配置是没有数据输出的，但是如果不想写这么长的配置怎么办呢？直接使用 `logging.basicConfig()` 进行一个简单的基础配置。

```
logging.basicConfig(
    level=logging.INFO,
    format='%(name)-25s %(asctime)s %(levelname)-8s %(lineno)-4d %(message)s',
    datefmt='[%Y %b %d %a %H:%M:%S]'
)
```

示例代码

```
# coding=utf-8

import sys
import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(lineno)-4d %(message)s', '%Y %b %d %a %H:%M:%S',)

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    logger.info("main start...")
    try:
        1 / 0
    except Exception as e:
        logger.exception("error %s", e)
    logger.info("main end.")

```

对比一下输出的日志即可看出。

使用 `logger.error` 的效果

```
__main__     2019 May 25 Sat 22:23:36 INFO     16   main start...
__main__     2019 May 25 Sat 22:23:36 ERROR    20   error integer division or modulo by zero
__main__     2019 May 25 Sat 22:23:36 INFO     21   main end.
```

使用 `logger.exception` 的效果

```
__main__     2019 May 25 Sat 22:23:52 INFO     16   main start...
__main__     2019 May 25 Sat 22:23:52 ERROR    20   error integer division or modulo by zero
Traceback (most recent call last):
  File "code/logging_exception.py", line 18, in <module>
    1 / 0
ZeroDivisionError: integer division or modulo by zero
__main__     2019 May 25 Sat 22:23:52 INFO     21   main end.
```
