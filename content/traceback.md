## traceback

```
traceback.print_stack()
```

打印堆栈信息


```
# coding=utf-8
import traceback
from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    traceback.print_stack()
    return 'hello world'


def main():
    app.run()


if __name__ == '__main__':
    main()

```


还有在运行中通过信号来打印堆栈信息

```
# -*- coding: utf-8 -*-
import traceback
import signal
import socket
import time


host = "127.0.0.1"
port = 8081

# s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# s.bind((host,port))
# s.listen(5)

print "Server is running on port %s Press Ctrl-C to stop"%port
signal.signal(signal.SIGUSR2, lambda num,stack:traceback.print_stack(stack))


while 1:
    time.sleep(10)
    print '10 seconds sheep'
    # clientsock, clientaddr = s.accept()
    # print "Welcome from %s:%s"%(clientaddr[0],clientaddr[1])
    # while 1:
    #     request = clientsock.recv(1024)
    #     print "Received From client : %r" % request
    #     if not request:
    #         break
    #     clientsock.send("Hello client:%s" % request)

```

socket 与 signal 似乎天生不和。

使用 flask 还是可以的

```
# -*- coding: utf-8 -*-
import signal
import traceback
from flask import Flask


app = Flask(__name__)
signal.signal(signal.SIGUSR2, lambda num,stack:traceback.print_stack(stack))


@app.route('/')
def index():
    traceback.print_stack()
    return 'hello world'


def main():
    app.run()


if __name__ == '__main__':
    main()

```

也可以使用 signal 做成一个可侵入式的 pdb

```
# -*- coding: utf-8 -*-
import signal
import pdb
from flask import Flask


app = Flask(__name__)
signal.signal(signal.SIGUSR2, lambda num,stack: pdb.set_trace())


@app.route('/')
def index():
    return 'hello world'


def main():
    app.run()


if __name__ == '__main__':
    main()

```

不过，因为 pdb 自身的问题，不能够引入新的变量。

但是，经过反复实现显示，应该不是 pdb 的问题，pdb 可以引入新的变量，导入类之类的事情，只是对已经编译好的函数新导入的类库无法使用。

```
# -*- coding: utf-8 -*-
import signal
import pdb
from flask import Flask

app = Flask(__name__)
signal.signal(signal.SIGUSR2, lambda num,stack: pdb.set_trace())


@app.route('/')
def index():
    return json.dumps({"name":"windard"})


def main():
    app.run()


if __name__ == '__main__':
    data = json.dumps({"name":"windard"})
    main()

```

但是这基本上没什么用，比如以上代码中，第12行的代码可以执行，但是到改函数执行的时候会报错，使用 pdb 侵入也无法改变；第20行的代码可以使用pdb导入json库来正常执行，但是第20行的错误无法通过编译，执行即报错，需使用 `python -m pdb ` 的方式来启动。
