## multiprocessing

### fork

多进程在 unix 类电脑上通常是由 fork 指定生成出来，但是在 Windows 上没有 fork 调用。

fork 生成子进程的时候，调用一次，返回两次.因为需要在子进程和父进程各返回一次，但是对于用户来说看起来像返回了两次。

第一次在父进程返回子进程 ID ，第二次子在进程返回 0。

```
Process (27939) start...
I (27939) just create a child process (27943)
I'm child process (27943) and my parent is (27939)
```

### process

基础的多进程库，可以进行一些简单的多进程操作.

多线程的处理和多进程是基本一致的，在 start 之后即开始子进程，在 join 之后才加入主进程阻塞主进程的继续。

默认创建的子进程并非守护进程，主进程会等待子进程结束后再终止，使用 `Process.daemon=True` 来创建守护进程。

```
# -*- coding: utf-8 -*-

from multiprocessing import Process
import os
import time


def sleeper(name, seconds):
    print 'starting child process with id: ', os.getpid()
    print 'parent process:', os.getppid()
    print 'sleeping for %s ' % seconds
    time.sleep(seconds)
    print "%s done sleeping" % name


if __name__ == '__main__':
    print "in parent process (id %s)" % os.getpid()
    p = Process(target=sleeper, args=('bob', 5))
    print 'daemon?', p.daemon
    p.daemon = not p.daemon
    print 'daemon?', p.daemon
    p.start()
    print "in parent process after child process start"
    print "parent process about to join child process"
    p.join()
    print "in parent process after child process join"
    print "parent process exiting with id ", os.getpid()
    print "The parent's parent process:", os.getppid()

```

使用 `multiprocessing.cpu_count()` 查看 CPU 个数

```
# coding=utf-8

from multiprocessing import Process, freeze_support

def process_data(filelist):
    for filepath in filelist:
        print('Processing {} ...'.format(filepath))
        # 处理数据
        # ...

if __name__ == '__main__':
    # 如果是在Windows下，还需要加上freeze_support()
    freeze_support()

    # full_list包含了要处理的全部文件列表
    full_list = [x for x in xrange(100)]

    n_total = len(full_list) # 一个远大于32的数
    n_processes = 32

    # 每段子列表的平均长度
    length = float(n_total) / float(n_processes)

    # 计算下标，尽可能均匀地划分输入文件列表
    indices = [int(round(i*length)) for i in range(n_processes+1)]

    # 生成每个进程要处理的子文件列表
    sublists = [full_list[indices[i]:indices[i+1]] for i in range(n_processes)]

    # 生成进程
    processes = [Process(target=process_data, args=(x,)) for x in sublists]

    # 并行处理
    for p in processes:
        p.start()

    for p in processes:
        p.join()
```

在 Linux 下可以使用 `multiprocessing.getppid` 来获得父进程的 pid ，但是在 Windows 下就不支持

```
# coding=utf-8

from multiprocessing import Process
import os
import time

def sleeper(name, seconds):
    print 'starting child process with id: ', os.getpid()
    # print 'parent process:', os.getppid()
    print 'sleeping for %s ' % seconds
    time.sleep(seconds)
    print "Done sleeping"

if __name__ == '__main__':
    print "in parent process (id %s)" % os.getpid()
    p = Process(target=sleeper, args=('bob', 5))
    p.start()
    print "in parent process after child process start"
    print "parent process about to join child process"
    p.join()
    print "in parent process after child process join"
    print "parent process exiting with id ", os.getpid()
    # print "The parent's parent process:", os.getppid()

```

### pool

进程池的默认大小是 CPU 的核数，但是这并不意味着进程池的最大值为 CPU 的核数。

使用 `apply_async` 异步创建进程，在子进程开始之后，主进程继续运行，创建的子进程不是守护进程。与 `map_async` 类似。

使用 `apply` 同步创建进程则会阻塞主进程的继续运行。与 `map` 类似。

进程池的 `join` 方法与进程类似，阻塞主进程，等待所有子进程完成后继续运行。调用 `join` 之前，必须 `close` 进程池，停止加入新的进程。

```
# -*- coding: utf-8 -*-

import os
import time
import random
import multiprocessing


def long_time_task(name):
    print 'Running task %s (%s)' % (name, os.getpid())
    start = time.time()
    time.sleep(random.random() * 5)
    end = time.time()
    print 'Task %s run %0.2f econds.' % (name, end - start)


if __name__ == '__main__':
    worker = multiprocessing.cpu_count()
    print 'Parent process %s' % os.getpid()
    print 'PC has %s CPU workers' % worker
    p = multiprocessing.Pool(worker)

    for i in range(10):
        p.apply_async(long_time_task, (i, ))
    print 'wait for all subprocess done.'
    p.close()
    print 'task start'
    p.join()
    print 'All task done.'

```

或者使用 map_async , 在进程池中有 callback 字段，可以返回线程结果,在普通的线程或者进程中，很难拿到返回的数据结果。


```
# -*- coding: utf-8 -*-

import os
import time
import random
import multiprocessing


def long_time_task(name):
    print 'Running task %s (%s)' % (name, os.getpid())
    start = time.time()
    time.sleep(random.random() * 5)
    end = time.time()
    spend = end - start
    print 'Task %s run %0.2f econds.' % (name, spend)
    return spend


if __name__ == '__main__':
    worker = multiprocessing.cpu_count()
    print 'Parent process %s' % os.getpid()
    print 'PC has %s CPU workers' % worker
    p = multiprocessing.Pool(worker)

    def callback(*args, **kwargs):
        print 'all process done', args, kwargs

    names = [i for i in range(10)]
    p.map_async(long_time_task, names, callback=callback)

    print 'wait for all subprocess done.'
    p.close()
    print 'task start'
    p.join()
    print 'All task done.'

```

因为在正常的 run 方法并不能返回数据的结果

```
# -*- coding: utf-8 -*-

import os
import time
import random
import multiprocessing


class MuProcess(multiprocessing.Process):

    def __init__(self, name):
        super(MuProcess, self).__init__()
        self.name = str(name)

    def run(self):
        print 'Running task %s (%s)' % (self.name, os.getpid())
        start = time.time()
        time.sleep(random.random() * 5)
        end = time.time()
        spend = end - start
        print 'Task %s run %0.2f econds.' % (self.name, spend)
        return spend


if __name__ == '__main__':
    print 'Parent process %s' % os.getpid()

    def callback(*args, **kwargs):
        print 'all process done', args, kwargs

    processes = map(lambda x: MuProcess(x), [i for i in range(10)])
    for p in processes:
        callback(p.start())
    print 'wait for all subprocess done.'
    for p in processes:
        p.join()
    print 'All task done.'

```

实际上，在线程池中，线程池本身就会返回线程的结果

```
# -*- coding: utf-8 -*-

import os
import time
import multiprocessing

def multi(x):
    return x + 42


if __name__ == '__main__':
    pool = multiprocessing.Pool()

    print pool.map(multi, range(10))
    print pool.map_async(multi, range(10)).get()

    for i in pool.imap_unordered(multi, range(10)):
        print i,

    print
    res = pool.apply_async(multi, (20, ))
    print res.get(timeout=20)

    res = pool.apply_async(os.getpid)
    print res.get()

    multiple_results = [pool.apply_async(os.getpid) for _ in range(4)]
    print [res.get() for res in multiple_results]

    res = pool.apply_async(time.sleep, (10, ))
    try:
        print res.get(timeout=1)
    except multiprocessing.TimeoutError:
        print 'we lacked patience and got a timeout error'

```

python2 中线程本身没有线程池，在 python3 才提供了线程池的支持。但是在 multiprocess 中有线程池的支持，还有一个 threadpool 的库提供线程池。

进程池是无序的，但是 threadpool 是有序的。

```
# -*- coding: utf-8 -*-

import os
import time
import random
import multiprocessing
from multiprocessing.pool import ThreadPool


def long_time_task(name):
    print 'Running task %s (%s)' % (name, os.getpid())
    start = time.time()
    time.sleep(random.random() * 5)
    end = time.time()
    print 'Task %s run %0.2f econds.' % (name, end - start)


if __name__ == '__main__':
    worker = multiprocessing.cpu_count()
    print 'Parent process %s' % os.getpid()
    print 'PC has %s CPU workers' % worker
    # p = multiprocessing.Pool(worker)
    p = ThreadPool()

    for i in range(10):
        p.apply_async(long_time_task, (i, ))
    print 'wait for all subprocess done.'
    p.close()
    print 'task start'
    p.join()
    print 'All task done.'

```

### threadpool

最简易的 threadpool 实现

```
# -*- coding: utf-8 -*-

import threading
from Queue import Queue
from random import randrange
from time import sleep


class Worker(threading.Thread):

    def __init__(self, tasks):
        super(Worker, self).__init__()
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kwargs = self.tasks.get()
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(e)
            finally:
                self.tasks.task_done()


class ThreadPool(object):
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in xrange(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kwargs):
        self.tasks.put((func, args, kwargs))

    def map(self, func, args_list):
        for args in args_list:
            self.add_task(func, args)

    def wait_completion(self):
        self.tasks.join()


if __name__ == '__main__':
    def wait_delay(d):
        print('sleep for (%d)sec' % d)
        sleep(d)


    delays = [randrange(3, 7) for i in range(50)]
    pool = ThreadPool(5)

    pool.map(wait_delay, delays)
    pool.wait_completion()

```

包括进程池在内的池，都是以队列的形式组成的。

使用线程池的话，map 的方法传入参数只能有一个，不能有多个入参，且传入顺序是随机的,并不是按照参数顺序。

还有一个库叫 threadpool

```
# -*- coding: utf-8 -*-

import threadpool

import os
import time
import random
import multiprocessing


def long_time_task(name):
    print 'Running task %s (%s)' % (name, os.getpid())
    start = time.time()
    time.sleep(random.random() * 5)
    end = time.time()
    print 'Task %s run %0.2f econds.' % (name, end - start)
    return end - start


if __name__ == '__main__':
    worker = multiprocessing.cpu_count()
    print 'Parent process %s' % os.getpid()
    print 'PC has %s CPU workers' % worker

    def callback(*args, **kwargs):
        print 'all process done', args, kwargs

    names = [i for i in range(10)]
    pool = threadpool.ThreadPool(worker)
    requests = threadpool.makeRequests(long_time_task, names, callback=callback)
    print 'wait for all subprocess done.'
    workers = [pool.putRequest(req) for req in requests]
    print 'task start'
    pool.wait()
    print 'All task done.'

```

然而连 `callback` 都用不了，返回的也不知道是什么，只知道还算能够使用。

### Queue

进程间通信一般采用 Queue 或 Pipes 等库来实现。

```
# -*- coding: utf-8 -*-

import time
import random

from multiprocessing import Queue, Process


def writeQ(q):
    for value in ['A', 'B', 'C', 'D', 'E']:
        print 'Put %s to queue ...' % value
        q.put(value)
        time.sleep(random.random())


def readQ(q):
    print 'read q and q status: ', q.empty()
    while not q.empty():
        print 'q is not empty'
        value = q.get()
        print 'Get %s from queue ...' % value
        time.sleep(random.random() * 2)


if __name__ == '__main__':
    q = Queue()
    pw = Process(target=writeQ, args=(q, ))
    pr = Process(target=readQ, args=(q, ))
    pw.start()
    time.sleep(0.001)
    pr.start()
    pw.join()
    pr.join()

```

1. Queue 自带线程锁，所以不用再额外加锁。但是如果是其他的共享数据，需要加锁，防止遭到破坏。
2. 如果读写在两个线程同时发生，则可能存在读取时线程为空的情况，读线程提前结束，所以最好写入队列的线程先行并耗时较短。
3. 如果需要读线程保证读取完毕，可以使用 `while True`, 然后手动结束读进程。
4. 但是手动终止有一个新的问题就是，不知道何时终止，可能主线程终止读进程的时候，还未读完队列中的数据。

```
# -*- coding: utf-8 -*-

import time
import random

from multiprocessing import Queue, Process


def writeQ(q):
    for value in ['A', 'B', 'C', 'D', 'E']:
        print 'Put %s to queue ...' % value
        q.put(value)
        time.sleep(random.random())


def readQ(q):
    while True:
        print 'read q and q status: ', q.empty()
        value = q.get()
        print 'Get %s from queue ...' % value
        time.sleep(random.random())


if __name__ == '__main__':
    q = Queue()
    pw = Process(target=writeQ, args=(q, ))
    pr = Process(target=readQ, args=(q, ))
    pw.start()
    pr.start()
    pw.join()
    # 死循环，手动终止
    pr.terminate()

```

或者等待队列为空再手动终止

> 但是这是和直接 `while not q.empty()` 效果是一样的，但理论上无济于事。

```
# -*- coding: utf-8 -*-

import time
import random

from multiprocessing import Queue, Process


def writeQ(q):
    for value in ['A', 'B', 'C', 'D', 'E']:
        print 'Put %s to queue ...' % value
        q.put(value)
        time.sleep(random.random())


def readQ(q):
    while True:
        print 'read q and q status: ', q.empty()
        value = q.get()
        print 'Get %s from queue ...' % value
        time.sleep(random.random() * 2)


if __name__ == '__main__':
    q = Queue()
    pw = Process(target=writeQ, args=(q, ))
    pr = Process(target=readQ, args=(q, ))
    pw.start()
    pr.start()
    pw.join()
    # 死循环，手动终止
    while True:
        if q.empty():
            pr.terminate()
            break

```

1. 线程锁和进程锁是不一样的
2. `Queue.Queue` 是线程安全的, `multiprocessing.Queue` 是进程安全的，不要混用，不能混用。

使用 `multiprocess.Pipe` 也能够在不同的进程间共享数据，但是它不是进程安全的，需要使用进程锁来保证数据安全性

Pipe 默认是全双工的，即返回两个通道都可读可写，如果是半双工的，则只能前一个通道读，后一个通道写。

```
# -*- coding: utf-8 -*-

import time
import random

from multiprocessing import Process, Pipe, Lock

l = Lock()


def writeQ(q):
    for value in ['A', 'B', 'C', 'D', 'E']:
        print 'Put %s to queue ...' % value
        q.send(value)
        time.sleep(random.random())


def readQ(q):
    for _ in range(2):
        l.acquire()
        print 'read q and q status: ', q.recv()
        l.release()


if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    pw = Process(target=writeQ, args=(child_conn, ))
    pr = Process(target=readQ, args=(parent_conn, ))
    pt = Process(target=readQ, args=(parent_conn, ))
    pw.start()
    pr.start()
    pt.start()

    # print 'from parent', parent_conn.recv()
    # child_conn.send('in parent')
    # child_conn.send('in parent')
    # print 'after parent', parent_conn.recv()

    pw.join()
    pr.join()
    pt.join()

```

### 进程变量

在进程之间无共享变量，不和线程一样，无论是全局变量，还是局部变量都是不能共享的。

```
# -*- coding: utf-8 -*-

from multiprocessing import Process


def change_global():
    global a
    a.append(1)
    print 'in global', a


def change_local(b):
    b.append(2)
    print 'in local', b


if __name__ == '__main__':
    a = []
    pg = Process(target=change_global)
    pg.start()
    pg.join()
    print a

    pl = Process(target=change_local, args=(a, ))
    pl.start()
    pl.join()
    print a

```

而如果将 `multiprocessing.Process` 换成 `threading.Thread` 则效果完全不一样。

所以进程之间的共享变量只能使用 `multiprocessing.Queue` 而不是 `Queue.Queue`

如果想在 `multiprocess.Queue` 使用 `Queue.Queue` 的功能，比如 `join` 或者 `task_done` 的功能就需要使用 `JoinableQueue`, 使用后者更快一些。

变量可以传入进程中，但是已经不是原来的模样。

因为在 python 中 GIL 的限制，在进程切换之间的消耗，其实并不建议使用多进程，可以使用协程或者异步来代替。

普通的局部变量或者全局变量不能共享，但是有专门的进程数据格式用来在不同的进程间同步数据,比如说 `multiprocess.Array` 和 `multiprocess.Value` , 注意在子进程中使用共享变量的时候，必须使用进程锁，不然很有可能会有问题，造成数据丢失甚至错误。

```
# -*- coding: utf-8 -*-

import multiprocessing


def decrease(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = - a[i]


if __name__ == '__main__':
    num = multiprocessing.Value('d', 0.0)
    arr = multiprocessing.Array('i', range(10))

    p = multiprocessing.Process(target=decrease, args=(num, arr))
    p.start()
    p.join()

    print(num.value)
    print(arr[:])

```

或者 `multiprocess.Manager`

```
# -*- coding: utf-8 -*-

import multiprocessing


def func(d, l):
    d[1] = '2'
    d['2'] = 2
    d[0.25] =None
    l.reverse()

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    d = manager.dict()
    l = manager.list(range(10))
    p = multiprocessing.Process(target=func, args=(d, l))
    p.start()
    p.join()

    print(d)
    print(l)

```

### lock
多进程间的共享变量，如果不用进程锁，就会造成数据混乱

```
# -*- coding: utf-8 -*-
from multiprocessing import Process, Manager, Lock
import os

manager = Manager()
sum = manager.Value('tmp', 0)
lock = Lock()


def testFunc(cc):
    # with lock:
    #     sum.value += cc
    sum.value += cc


if __name__ == '__main__':
    ps = []

    for ll in range(100):
        t = Process(target=testFunc, args=(1,))
        ps.append(t)

    for i in range(len(ps)):
        ps[i].start()

    for j in range(len(ps)):
        ps[j].join()

    print "------------------------"
    print 'process id:', os.getpid()
    print sum.value

```

如果不使用进程锁，得到的数据永远都小于100，使用进程锁之后才能得到想要的结果。

多进程中的 Queue 和消息队列中的 Queue 有什么区别?

线程池和进程池有什么区别？

### 信号量

进程锁内部就是一个大小为1的信号量，可重用进程锁是大小不固定的信号量，而信号量可以设置固定大小。

设置一个固定大小的信号量，可以开启十个子进程，去争夺两个信号，同时最多只能由两个子线程在运行。

线程信号量与进程信号量是一样的。

```
# -*- coding: utf-8 -*-

import threading
import time
semaphore = threading.Semaphore(2)


def worker(id):
    print 'thread {id} acquire semaphore'.format(id=id)
    semaphore.acquire()
    print 'thread {id} get semaphore do something'.format(id=id)
    time.sleep(2)
    semaphore.release()
    print 'thread {id} release semaphore'.format(id=id)


if __name__ == '__main__':

    for i in range(10):
        t = threading.Thread(target=worker, args=(i, ))
        t.start()

```


### v2ex

在 v2ex 里看到这样一个问题，让以下代码中的 my_process 只运行一次，即 my_progress 在多进程的情况下只运行一次，也就是同时只有一个 printx 在运行。

```
from multiprocessing import Process
import time

class ScheduleTest():
    @staticmethod
    def printx():
        while True:
            print('hello x')
            time.sleep(5)

    def run(self):
        print('printx is running...')
        my_process = Process(target=self.printx)
        my_process.start()


def app_run():
    my_schedule = ScheduleTest()
    process_0 = Process(target=my_schedule.run)
    process_1 = Process(target=my_schedule.run)
    process_2 = Process(target=my_schedule.run)
    process_0.start()
    process_1.start()
    process_2.start()


if __name__ == '__main__':
    app_run()
```

#### 进程锁

进程锁的位置很重要

```
# -*- coding: utf-8 -*-
from multiprocessing import Process, Lock
import time


lock = Lock()

class ScheduleTest():
    @staticmethod
    def printx():
        while True:
            print('hello x')
            time.sleep(5)

    def run(self):
        print('printx is running...')
        my_process = Process(target=self.printx)
        my_process.start()


def app_run():
    my_schedule = ScheduleTest()
    for i in range(3):
        with lock:
            p = Process(target=my_schedule.run)
            p.start()
            p.join()


if __name__ == '__main__':
    app_run()

```

#### 信号量

信号量其实也是进程锁

```
# -*- coding: utf-8 -*-
from multiprocessing import Process, Semaphore
import time


s = Semaphore(1)


class ScheduleTest():
    @staticmethod
    def printx():
        while True:
            print('hello x')
            time.sleep(5)

    def run(self):
        s.acquire()
        print('printx is running...')
        my_process = Process(target=self.printx)
        my_process.start()
        my_process.join()
        s.release()


def app_run():
    my_schedule = ScheduleTest()
    process_0 = Process(target=my_schedule.run)
    process_1 = Process(target=my_schedule.run)
    process_2 = Process(target=my_schedule.run)
    process_0.start()
    process_1.start()
    process_2.start()


if __name__ == '__main__':
    app_run()

```

#### 进程锁就是信号量

进程锁就是大小为1的信号量

```
# -*- coding: utf-8 -*-

from multiprocessing import Process, Lock
import time

lock = Lock()


class ScheduleTest():
    @staticmethod
    def printx():
        while True:
            print('hello x')
            time.sleep(5)

    def run(self):
        with lock:
            print('printx is running...')
            my_process = Process(target=self.printx)
            my_process.start()
            my_process.join()


def app_run():
    my_schedule = ScheduleTest()
    process_0 = Process(target=my_schedule.run)
    process_1 = Process(target=my_schedule.run)
    process_2 = Process(target=my_schedule.run)
    process_0.start()
    process_1.start()
    process_2.start()


if __name__ == '__main__':
    app_run()
```

#### 共享变量

共享变量注意需加锁

```
# -*- coding: utf-8 -*-
from multiprocessing import Process, Manager, Lock
import time

manager = Manager()
sum = manager.Value('tmp', 0)
lock = Lock()


class ScheduleTest():
    @staticmethod
    def printx():
        while True:
            print('hello x')
            time.sleep(5)

    def run(self):
        with lock:
            if not sum.value:
                print('printx is running...')
                my_process = Process(target=self.printx)
                my_process.start()
                sum.value += 1
            else:
                print('printx has ran.')


def app_run():
    my_schedule = ScheduleTest()
    process_0 = Process(target=my_schedule.run)
    process_1 = Process(target=my_schedule.run)
    process_2 = Process(target=my_schedule.run)
    process_0.start()
    process_1.start()
    process_2.start()


if __name__ == '__main__':
    app_run()

```

### 参考链接

[multiprocess](https://docs.python.org/2/library/multiprocessing.html)

[Python并行编程 中文版](http://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/index.html)

[理解Python并发编程一篇就够了 - 线程篇](http://www.dongwm.com/archives/%E4%BD%BF%E7%94%A8Python%E8%BF%9B%E8%A1%8C%E5%B9%B6%E5%8F%91%E7%BC%96%E7%A8%8B-%E7%BA%BF%E7%A8%8B%E7%AF%87/)

[理解Python并发编程一篇就够了 - 进程篇](http://www.dongwm.com/archives/%E4%BD%BF%E7%94%A8Python%E8%BF%9B%E8%A1%8C%E5%B9%B6%E5%8F%91%E7%BC%96%E7%A8%8B-%E8%BF%9B%E7%A8%8B%E7%AF%87/)
