## statsd

### 简介

pystatsd 和 statsdpy

前者是客户端，后者是服务器端。用来做服务监控，主要是服务打点和耗时统计。

StatsD 一开始是一个 node 服务，后来有人用 C 实现了一个，就是 statsdpy ，只是因为作为 python 库，就成了 python 服务，其实在 pystatsd 有人用纯 python 实现了一个。

StatsD 客户端与服务器端之间的交互通过 udp 请求来完成，端口号为 8125.

> node 的 StatsD 的原生实现也支持 8126 的 tcp 端口
> StatsD 的数据存储支持多种服务，如 graphite, influxdb, ganglia 之类的

### 关于数据

graphite 分为三个部分

- carbon 守护进程服务，用来与外部数据交互，包括数据传入与导出
- whisper 时序数据库，存储打点数据
- graphite-web 基于 Django 的 web 管理后台

1. 实际数据最终都落到 graphite 上
2. graphite 中 carton 为数据交互端，监听端口 2003，基于 tcp 协议。
3. statsd 的服务器端其实就是将数据传到 graphite 上，pystatsd 也自带一个小小的服务器端
4. graphite 中数据读取端口即 graphite-web 管理后台端口

> 好吧，其实 pystatsd 有两个人实现了，本文所指是 [pystatsd](https://github.com/sivy/pystatsd), 而非 [pystatsd](https://github.com/jsocol/pystatsd) 或其他


使用

```
sudo ngrep -qd any . udp dst port 8125
```

监控到 statsd 的服务器端的数据

使用

```
sudo ngrep -qd any stats tcp dst port 2003
```

监控到 graphite 的服务器端的数据

### pystatsd

pystatsd client

```
# coding=utf-8
from pystatsd import Client

sc = Client('example.org',8125)

sc.timing('python_test.time',500)
sc.increment('python_test.inc_int')
sc.decrement('python_test.decr_int')
sc.gauge('python_test.gauge', 42)
```

pystatsd server

```
# coding=utf-8
from pystatsd import Server

srvr = Server(debug=True)
srvr.serve()
```

可以在需要的地方使用 Server ，也可以不用。

### statsd

statsd 这个库也可以用

```
# -*- coding: utf-8 -*-
import time
import random
from statsd import StatsClient
import functools

statsd = StatsClient()

@statsd.timer('myfunc')
def myfunc(a, b):
    statsd.incr("key.incr")
    time.sleep(random.random())


def time_deco(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        statsd.timing('krpc.{}'.format(func.__name__),
                      1000.0 * (time.time() - start_time))
    return wrap


@time_deco
def hello():
    time.sleep(random.random())


if __name__ == '__main__':
    for i in range(100000):
        time.sleep(random.random() / 10)
        # myfunc(1, 1)
        hello()

```

### 协议实现

#### graphite

```
metric_path value timestamp\n
```

- metric_path 指标路径
- value 指标的值
- timestamp 时间戳

可以手动往 graphite 打数据。

```
echo "test.count 4 `date +%s`" | nc 127.0.0.1 2003
```

数据在 StatsD 每十秒做一次聚合，算出数据的平均值发送给 graphite

#### StatsD

```
<bucket>:<value>|<type>[|@sample_rate]
```

- bucket 每一个 metric 的标识，即每一个打点的变量
- value 每一个 metric 的值
- type 每一个 metric 的类型，通常有timer、counter、gauge 和 set 四种
- sample_rate 打点频率，降低采样频率，提高服务器性能。

metric 即打点，metric 的类型
- counter 计数器，用来对一个数据进行加减计数
- timer 计时器，对一个操作进行计算耗时，还会计算耗时的平均值，最大值，最小值等
- gauge 标量，一段操作内的计数器，可以进行重置
- set 设置值，每次都是设置一个的值

一个示例

```
echo "foo:1|c" | nc -u -w0 127.0.0.1 8125
```


### 参考文章

[StatsD 的使用小结][https://juejin.im/entry/58f6d239a0bb9f006ab4ac2f]

[Graphite Documentation](https://graphite.readthedocs.io/en/latest/index.html)

[Welcome to Python StatsD’s documentation!](https://statsd.readthedocs.io/en/v3.3/index.html)
