## gevent

python 中的协程库，虽然可以使用 `yield` 实现最基础的协程功能，但是还是使用封装起来的库比较方便。

因为 python GIL 的原因，在底层实现的时候还是只有一个线程在执行，但是 gevent 在 io 层快速切换，使用协程交替执行就是比单线程顺序执行要快一些。

gevent 能够获得极高的并发性能，但是只能在 Linux/Unix 下运行，Windows 下无法使用。已经习惯了，同样的并发库，在 Windows 下能用的只有 Select 。

### 重要的一点

gevent 是通过底层第三方库 greenlet 来实现协程，我们并不用直接使用 greenlet ，它是在 io 操作时通过 greenlet 进行自动切换，尽量减少 io 的时间。因为 io 操作非常费时，所以实际使用的并发效果非常明显。

由于切换是在 IO 操作时自动完成，所以需要使用 gevent修改一下 python 自带的标准库，这一过程可以在启动的时候通过 `monkey.patch_all` 完成

```
from gevent import monkey

monkey.patch_all()

```

### 简单的例子

```
# coding=utf-8

import time
import gevent
from gevent import  monkey

monkey.patch_all()


def spend_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        rv = func(*args, **kwargs)
        end_time = time.time()
        print end_time - start_time
        return rv
    return wrapper


def daemon():
    time.sleep(1)
    print 'done'


@spend_time
def in_order():
    for i in xrange(3):
        daemon()


@spend_time
def in_concur():
    spawns = []
    for i in xrange(3):
        spawns.append(gevent.spawn(daemon))
    gevent.joinall(spawns)


def main():
    in_order()
    in_concur()


if __name__ == '__main__':
    main()

```

输出

```
done
done
done
3.01224112511
done
done
done
1.00596690178
```

并发执行，耗时直接降到三分之一，这还没有大量的 io 等待，那我们实现有一个有网络请求的并发例子，使用效果更加明显。

```
# coding=utf-8

import time
from gevent import monkey
import gevent
import urllib2


monkey.patch_all()


def spend_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        rv = func(*args, **kwargs)
        end_time = time.time()
        print end_time - start_time
        return rv
    return wrapper


def request(url):
    print('GET: %s' % url)
    resp = urllib2.urlopen(url)
    data = resp.read()
    print('%d bytes received from %s.' % (len(data), url))


@spend_time
def in_order(urls):
    for url in urls:
        request(url)


@spend_time
def in_concur(urls):
    spawns = []
    for url in urls:
        spawns.append(gevent.spawn(request, url))

    gevent.joinall(spawns)


def main():
    urls = ['https://baidu.com', 'https://zhihu.com', 'https://ele.me']
    in_order(urls)
    in_concur(urls)


if __name__ == '__main__':
    main()

```


输出

```
GET: https://baidu.com
111574 bytes received from https://baidu.com.
GET: https://zhihu.com
11878 bytes received from https://zhihu.com.
GET: https://ele.me
1356 bytes received from https://ele.me.
0.801009178162
GET: https://baidu.com
GET: https://zhihu.com
GET: https://ele.me
1356 bytes received from https://ele.me.
111562 bytes received from https://baidu.com.
11878 bytes received from https://zhihu.com.
0.321052074432
```

可以看到三次请求时并发执行，最终完成的先后顺序也并不一定是开始的顺序，减少了大量的等待，速度翻倍。

在实际使用中，可以很方便的引入 gevent 进行并发操作，就能获得大量的性能优化。


### flask 性能优化

```
# coding=utf-8

from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    return 'hello world'


if __name__ == '__main__':
    app.run()

```

输出

```
Transactions:               6862 hits
Availability:              86.12 %
Elapsed time:              34.69 secs
Data transferred:           0.07 MB
Response time:              0.20 secs
Transaction rate:         197.81 trans/sec
Throughput:             0.00 MB/sec
Concurrency:               39.71
Successful transactions:        6862
Failed transactions:            1106
Longest transaction:            7.53
Shortest transaction:           0.00
```

开启多线程优化

```
# coding=utf-8

from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    return 'hello world'


if __name__ == '__main__':
    app.run(threaded=True)

```

输出

```

Transactions:               6481 hits
Availability:              85.60 %
Elapsed time:              30.60 secs
Data transferred:           0.07 MB
Response time:              0.19 secs
Transaction rate:         211.80 trans/sec
Throughput:             0.00 MB/sec
Concurrency:               41.07
Successful transactions:        6481
Failed transactions:            1090
Longest transaction:            7.47
Shortest transaction:           0.01
```

使用 gevent 优化

```
# coding=utf-8

from flask import Flask
from gevent.pywsgi import WSGIServer


app = Flask(__name__)


@app.route('/')
def index():
    return 'hello world'


if __name__ == '__main__':
    http = WSGIServer(('', 5000), app)
    http.serve_forever()

```

输出

```
Transactions:              25036 hits
Availability:              98.18 %
Elapsed time:              47.64 secs
Data transferred:           0.26 MB
Response time:              0.41 secs
Transaction rate:         525.52 trans/sec
Throughput:             0.01 MB/sec
Concurrency:              213.98
Successful transactions:       25036
Failed transactions:             464
Longest transaction:           20.41
Shortest transaction:           0.00
```

性能的提升有目共睹