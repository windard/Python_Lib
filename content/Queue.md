## Queue

队列库，队列就是先进先出(First Input First Output)型的一种数据结构，但是这个库也可以表示栈，就是先进后出型(Last Input First Output)的数据结构，不仅如此，还有一种按优先级别的队列结构。

队列一般用于解决多线程问题，在生产者消费者模式中经常用到。队列操作是原子性的，队列是线程安全的，不能保证进程安全，`multiprocessing.Queue` 保证进程安全。

队列只支持浅拷贝，不支持深拷贝，如果想用深拷贝的话可以使用 heapq

或者用到 列表 也可以实现队列的功能，append 和 pop 函数

#### 它们分别的类是：

```python
Queue.Queue(maxsize=0)                    FIFO
Queue.LifoQueue(maxsize=0)                LIFO
Queue.PriorityQueue(maxsize=0)            优先级别队列
```

#### 这个库中的常用方法：（通用）
1. Queue.qsize()                                    返回队列已用大小

1. Queue.empty()                                    返回队列是否为空

1. Queue.full()                                     返回队列是否为满

1. Queue.put(item[,block[,timeout]])                往队列中加入数据
>block为False或者是True，表示是否为阻塞型，默认为True，timeout为如果阻塞最多等待时间，默认为None。
>阻塞型，如果队列为非空，如果为设定timeout，则阻塞进程等待空闲为止，如果设定了timeout，超时仍未空闲则报错。
>非阻塞型，如果队列为非空，则报错。
5. Queue.put_nowait(item)                           往队列中写入数据
>即 Queue.put()  非阻塞型
6. Queue.get([block[,timeout]])                     从队列中取得数据
>默认block为True,timeout为None
7. Queue.get_nowait()                               从队列中取得数据
> 即 Queue.get()  非阻塞型
8. Queue.join()                                     将队列加入主线程
>将队列加入主线程之后，即主线程等该任务结束之后再进行下一个任务，阻塞线程的继续。

#### Queue

因为 Queue 是线程安全的，所以在多线程中用来同步数据。
- Queue.not_empty 和 Queue.empty() 严格来说是不一样的，前者是 `_threading.Condition` ，后者是计算 `Queue._qsize` 不过两者都可以用来判断队列是否已满，两者都是原子操作，线程安全的，not_empty 还是一个上下文管理器，可以作为一个线程锁来使用。
- Queue.task_done 在完成一项工作后，给队列计数器减一，如果不进行这项操作，从队列中取出数据队列仍不知，使用 join 则会永久阻塞进程，常用消费者线程中使用
- Queue.join 阻塞主线程，在队列结束后再继续执行。task_done 和 join 是一起使用的，只有使用 task_done 表示从队列中取出数据成功之后，join 阻塞主线程才知道结束，否则会一直阻塞不会结束。

```
# -*- coding: utf-8 -*-

import time
import Queue
import threading


def write(q):
    for i in range(10):
        q.put(i)
        print 'put', i


def read(q):
    while 1:
        time.sleep(0.5)
        print 'get', q.get()
        # q.task_done()


if __name__ == '__main__':
    q = Queue.Queue()
    threads = []
    threads.append(threading.Thread(target=write, args=(q, )))
    threads.append(threading.Thread(target=read, args=(q, )))
    for t in threads:
        t.setDaemon(True)
        t.start()
    q.join()
    print 'queue done. '
```

- 将消费者和生产者都设置为守护线程，为了消费者进程阻塞主进程结束
- 将消费者时间设置长一些，为了保证消费者不会提前导致队列为空，程序结束。

这样就可以看到 task_done 可以引导队列结束并终止主流程。

为什么不用

```
    while 1:
        time.sleep(0.5)
        if q.empty():
            break
        print 'get', q.get()
        # q.task_done()
```

或者

```
    while q.not_empty:
        time.sleep(0.5)
        print 'get', q.get()
        # q.task_done()

```

之类的结束消费者进程,因为消费者和生产者之间的耗时不一定，且 empty 的判断也不一定准确，可能在消费者快于生产者的情况下，队列有可能为空。

在消费者快于生产者的情况下，队列随时可能为空，如何准确的识别程序结束

1. 判断线程数，如果生产者线程全部结束，即可认为程序已经结束，或者几近结束 (不准确，忽略了消费者耗时)
2. 从队列中取数据设置超时时间，阻塞消费者。
3. 在消费者完成的最后添加一个特殊标志，不过需注意数量要匹配上消费者的数目

在以上三种方式中，都不再需要 task_done 和 join ，线程也最好是非守护线程。不过如果有这种需求，可以考虑使用消息队列的发布订阅模型，而不是队列的生产者消费者模型。

```
# -*- coding: utf-8 -*-

import time
import Queue
import threading


def write(q):
    for i in range(10):
        q.put(i)
        print 'put', i
        time.sleep(1)

    q.put(None)


def read(q):
    while 1:
    # while q.not_empty:
        time.sleep(0.5)
        # if q.empty():
        #     break
        item = q.get()
        print 'get', item
        if item == None:
            break
        # q.task_done()


if __name__ == '__main__':
    q = Queue.Queue()
    threads = []
    threads.append(threading.Thread(target=write, args=(q, )))
    threads.append(threading.Thread(target=read, args=(q, )))
    for t in threads:
        # t.setDaemon(True)
        t.start()
    # q.join()

```

#### 一个小例子

```python


import Queue

#FIFO
a = Queue.Queue(4)
a.join()

for i in range(4):
	a.put(i)

for i in range(4):
	print a.get(),
	a.task_done()

print

b = Queue.LifoQueue(4)
b.join()

for i in range(4):
	b.put(i)

for i in range(4):
	print b.get(),
	b.task_done()
```

保存为queue_demo.py，运行，看一下结果。

![queue_demo.jpg](images/queue_demo.jpg)


#### 队列的遍历

```


import Queue

t = Queue.Queue()
t.put({0:"0000"})
t.put({1:"0001"})
t.put({2:"0010"})

try:
    while not t.empty():
        print t.get()
except Exception,e:
    print e
```

运行结果

```
windard@windard:~/Desktop/python$ python test.py
{0: '0000'}
{1: '0001'}
{2: '0010'}

```


#### 分布式消息队列

queue_manager.py

```
# -*- coding: utf-8 -*-

import random
import Queue

from multiprocessing.managers import BaseManager


class QueueManager(BaseManager):
    pass


if __name__ == '__main__':

    task_queue = Queue.Queue()
    result_queue = Queue.Queue()


    QueueManager.register('get_task_queue', callable=lambda :task_queue)
    QueueManager.register('get_result_queue', callable=lambda :result_queue)

    manager = QueueManager(address=('', 5000), authkey='abc')

    manager.start()


    task = manager.get_task_queue()
    result = manager.get_result_queue()

    for i in range(10):
        n = random.randrange(100)
        print 'put task %s ...' % n
        task.put(n)

    print 'try get result ...'

    for i in range(10):
        r = result.get(timeout=10)
        print 'result is %s' % r

    manager.shutdown()

```


queue_worker.py

```
# -*- coding: utf-8 -*-

import time
import Queue

from multiprocessing.managers import BaseManager


class QueueManager(BaseManager):
    pass


if __name__ == '__main__':

    QueueManager.register('get_task_queue')
    QueueManager.register('get_result_queue')

    server_addr = ('127.0.0.1', 5000)

    print 'connect to server %s:%d ...' % server_addr

    m = QueueManager(address=server_addr, authkey='abc')
    m.connect()

    task = m.get_task_queue()
    result = m.get_result_queue()


    for i in range(10):
        try:
            n = task.get(timeout=1)
            print 'run task %d * %d' % (n, n)
            r = '%d * %d = %d' % (n, n, n * n)
            time.sleep(n * 0.1)
            result.put(r)
        except Queue.Empty:
            print 'task queue is empty'

    print 'worker exit.'

```


### 参考链接

[使用 Python 进行线程编程](https://www.ibm.com/developerworks/cn/aix/library/au-threadingpython/)
