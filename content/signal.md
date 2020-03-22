## signal

信号量模块，一般信号量的操作用来解决同步与异步的问题，避免死锁。同样的，Windows 下的功能不齐全，最好在 Linux 下。

### 简单示例

```
# -*- coding: utf-8 -*-

import signal
import os
import time


def receive_signal(signum, stack):
    print 'Received:', signum


if __name__ == '__main__':

    # Register signal handlers
    signal.signal(signal.SIGUSR1, receive_signal)
    signal.signal(signal.SIGUSR2, receive_signal)

    # Print the process ID so it can be used with 'kill'
    # to send this program signals.
    print 'My PID is:', os.getpid()

    while True:
        print 'Waiting...'
        time.sleep(3)

```

信号量通常使用在多线程或多进程中传递信号。

常见的信号比如

```
SIGINT  - `Ctrl` + `C` 就是 KeyboardInterrupt     # 2
SIGQUIT - `Ctrl` + `\`                           # 3
SIGSTOP - `Ctrl` + `Z`                           # 17
SIGKILL - None                                   # 9
```

可以使用 `kill -2 xx` 或者 `kill -INT xx` 或者 `Ctrl` + `C` 来传输信号量

接收键盘输入信号

```
# -*- coding: utf-8 -*-

import signal
import os


def do_exit(sig, stack):
    raise SystemExit('Exiting')


signal.signal(signal.SIGINT, signal.SIG_IGN)
signal.signal(signal.SIGUSR1, do_exit)

print 'My PID:', os.getpid()

signal.pause()  # 当接受到键盘的时候，signal.SIG_IGN给忽略了
print 'End of Exit'

```

或者这样

```
# -*- coding: utf-8 -*-

import signal
import os
import time


def receive_signal(signum, stack):
    print 'Received:', signum


def receive_exit(signum, stack):
    print 'Exit'
    raise SystemExit('Exiting')


if __name__ == '__main__':

    # Register signal handlers
    signal.signal(signal.SIGINT, receive_signal)
    signal.signal(signal.SIGQUIT, receive_signal)

    # SIGSTOP, SIGKILL can't received message
    # signal.signal(signal.SIGSTOP, receive_signal)
    # signal.signal(signal.SIGKILL, receive_exit)

    print 'My PID is:', os.getpid()

    while True:
        print 'Waiting...'
        time.sleep(3)

```

### 所有信号

```
# -*- coding: utf-8 -*-

import signal


def alarm_received(n, stack):
    return


signal.signal(signal.SIGALRM, alarm_received)


# SIG_ING 如果信号被忽略
# SIG_DFL 如果使用默认行为
# SIG_IGN -- if the signal is being ignored
# SIG_DFL -- if the default action for the signal is in effect
# None -- if an unknown handler is in effect
# anything else -- the callable Python object used as a handler
signals_to_names = dict(
    (getattr(signal, n), n)
    for n in dir(signal)
    if n.startswith('SIG') and '_' not in n
)

for s, name in sorted(signals_to_names.items()):
    handler = signal.getsignal(s)
    if handler is signal.SIG_DFL:
        handler = 'SIG_DFL'
    elif handler is signal.SIG_IGN:
        handler = 'SIG_IGN'
    print '%-10s (%2d):' % (name, s), handler

```

### 使用示例

使用 signal.alarm 是会持续一段时间的，使用这个特性可以用来做定时器。

```
# -*- coding: utf-8 -*-

import time
import signal


# After finish alarm
def receive_alarm(signum, stack):
    print 'Alarm :', time.ctime()


# Call receive_alarm with 2 seconds
signal.signal(signal.SIGALRM, receive_alarm)
print 'Before:', time.ctime()

# Unix only
signal.alarm(2)
print 'After alarm :', time.ctime()

# Alarm will finish sleep
time.sleep(3)
print 'After sleep :', time.ctime()

```

### 官方示例

```
# -*- coding: utf-8 -*-

import os
import signal

# 定义一个信号处理函数，该函数打印收到的信号，然后raise IOError
def handler(signum, frame):
    print 'Signal handler called with signal', signum
    raise IOError("Couldn't open device!")

# 对SIGALRM(终止)设置处理的handler, 然后设置定时器，5秒后触发SIGALRM信号
signal.signal(signal.SIGALRM, handler)
signal.alarm(5)

# open 操作可能异常等待
fd = os.open('/dev/ttys0', os.O_RDWR)

signal.alarm(0)          # 关闭定时器

```

该示例实现的功能是，为了防止打开一个文件出错或者其他异常一直处于等待的状态，设定一个定时器，5秒后触发IOError。如果5s内正常打开文件，则清除定时器。

还可以用来做超时器

```
# -*- coding: utf-8 -*-

import signal
import requests


def timeoutFn(func, args=(), kwargs={}, timeout_duration=5, default=None):

    class TimeoutError(Exception):
        pass

    def handler(signum, frame):
        raise TimeoutError()

    # set the timeout handler
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout_duration)
    try:
        result = func(*args, **kwargs)
    except TimeoutError as exc:
        result = default
    finally:

        signal.alarm(0)
        signal.signal(signal.SIGALRM, signal.SIG_DFL)
    return result


if __name__ == '__main__':
    print timeoutFn(requests.get, ("https://baidu.com", ), default='failed')
    print timeoutFn(requests.get, ("https://google.com", ), default='failed')

```

使用超时器，可以制作一个超时重试的装饰器。

就像这样

```
# -*- coding: utf-8 -*-

import signal
import requests
import functools


def timeoutFn(func, args=(), kwargs={}, timeout_duration=2, default=None):

    class TimeoutError(Exception):
        pass

    def handler(signum, frame):
        raise TimeoutError()

    # set the timeout handler
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout_duration)
    try:
        result = func(*args, **kwargs)
    except TimeoutError as exc:
        result = default
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, signal.SIG_DFL)
    return result


def timeout_retry(try_times=3, timeout=3, default=None):
    class TimeoutError(Exception):
        pass

    def handler(signum, frame):
        raise TimeoutError()

    def decorate(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            time_left = try_times
            while time_left > 0:
                signal.signal(signal.SIGALRM, handler)
                signal.alarm(timeout)
                try:
                    result = func(*args, **kwargs)
                except TimeoutError as e:
                    time_left -= 1
                else:
                    return result
                finally:
                    signal.alarm(0)
                    signal.signal(signal.SIGALRM, signal.SIG_DFL)
            return default
        return wrapper
    return decorate


@timeout_retry(timeout=5, default='failed')
def request(url):
    return  requests.get(url)


if __name__ == '__main__':
    # print timeoutFn(requests.get, ("https://baidu.com", ), default='failed')
    # print timeoutFn(requests.get, ("https://yahoo.com", ), default='failed')
    print request("https://baidu.com")
    print request("http://127.0.0.1:5000/")

```
