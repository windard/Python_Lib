## threading

#### 基本使用

在 thread 的库里还需要我们自己的去设定锁，并且在主线程里阻塞主线程的进行来判断锁是否已经释放, threading 是比 thread 更高级易于操作的多线程库。

多线程中，子线程默认不是守护线程，主线程会等待子线程结束再结束。如果要设为守护线程则在主线程结束后即终止 `threading.Thread.setDaemon(True)`.

多线程中，子线程创建后，`start` 即开始子线程，主线程继续进行，`join` 即阻塞主线程，等待子线程结束后再继续主线程。

在手动的将子线程加入(join)到主线程中后，主线程就会等待子线程全部结束才会继续 join 之后的程序。

在 `join` 被加入到主线程之后，虽然主线程被阻塞，但是并不影响其他线程，其他线程可以继续 `join` 到主线程。

在未设置守护线程，未 `join` 到主线程中的时候，主线程会先运行结束，但是主程序未结束，等待子线程结束后程序才会结束。

守护线程的意思就是说这个线程独立于主线程，主线程可以先于守护线程结束而不用等候守护线程结束。

```
# -*- coding: utf-8 -*-

from threading import Thread
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
    p = Thread(target=sleeper, args=('bob', 5))
    print 'daemon?', p.isDaemon()
    p.setDaemon(not p.isDaemon())
    print 'daemon?', p.isDaemon()
    p.start()
    print "in parent process after child process start"
    print "parent process about to join child process"
    p.join()
    print "in parent process after child process join"
    print "parent process exiting with id ", os.getpid()
    print "The parent's parent process:", os.getppid()

```

还是上一个例子，我们用threading来试一下。

```python
# coding=utf-8

import threading
from time import ctime,sleep

def loop(nloop,nsec):
	print "loop",nloop," start at: ",ctime()
	sleep(nsec)
	print "loop",nloop,"end    at: ",ctime()

print "all start at: ",ctime()
loops = [4,2]
threads = []
nloops = range(len(loops))

#创建两个线程
for i in nloops:
	t = threading.Thread(target=loop,args=(i,loops[i]))
	threads.append(t)

#让两个线程同时开始
for i in nloops:
	threads[i].start()

#将两个线程加入主线程
#如果将join和start在一起的话
#就会阻塞主线程的执行
#没有产生另一个子线程
#所以并没有开启多线程
#还是一个线程一个线程的执行
for i in nloops:
	threads[i].join()

print "all end   at: ",ctime()
```

保存为threading_demo.py，运行，看一下结果。

![threading_demo.jpg](images/threading_demo.jpg)

```python
# coding=utf-8

import threading
from time import ctime,sleep

def loop(nloop,nsec):
    print "loop",nloop," start at: ",ctime()
    sleep(nsec)
    print "loop",nloop,"end    at: ",ctime()

print "all start at: ",ctime()
loops = [4,2]
threads = []
nloops = range(len(loops))

#创建两个线程
for i in nloops:
    t = threading.Thread(target=loop,args=(i,loops[i]))
    t.setDaemon(False)
    threads.append(t)

#让两个线程同时开始
for i in nloops:
    threads[i].start()

print "all end   at: ",ctime()
```

这样的写法与上面的效果一致。

#### 创建多线程的几种方法

上面我们演示的是最基本的创建多线程的方式，也是最不推荐的方式。实际上threading库一共为我们提供三种创建多线程的方法，后两种更加的体现了Python面向对象的特性。

三种创建多线程的方法
1. 创建一个threading的实例，传给它一个参数。
2. 创建一个threading的实例，传给它一个可调用的类对象。
3. 从threading派生出一个子类，创建这个子类的实例。

那么接下里我们分别演示一下另外的两种方法。

###### 创建一个threading的实例，传给它一个可调用的类对象
这里我们需要先创建一个类供线程启动的时候执行，然后在线程启动的时候，Thread对象会调用我们创建的对象的执行函数。

```python
# coding=utf-8

import threading
from time import ctime,sleep

class ThreadFunc(object):
	def __init__(self, func ,args,name=""):
		self.args = args
		self.func = func
		self.name = name

	def __call__(self):
		apply(self.func,self.args)

def loop(nloop,nsec):
	print "loop",nloop," start at: ",ctime()
	sleep(nsec)
	print "loop",nloop,"end    at: ",ctime()

print "all start at: ",ctime()

loops = [4,2]
threads = []
nloops = range(len(loops))

for i in nloops:
	t = threading.Thread(target=ThreadFunc(loop,(i,loops[i]),loop.__name__))
	threads.append(t)

for i in nloops:
	threads[i].start()

for i in nloops:
	threads[i].join()

print "all end   at: ",ctime()
```

保存为threading_class.py，运行，看一下结果。

![threading_class.jpg](images/threading_class.jpg)

#### 从threading派生出一个子类，创建这个子类的实例
创建一个继承自Thread的之类，然后构造这个之类的实例，这时，Thread的start方法在就要在之类里重写为run方法。

```python
# coding=utf-8

import threading
from time import ctime,sleep

class MyThread(threading.Thread):
	def __init__(self,func,args,name=""):
		threading.Thread.__init__(self)
		self.name = name
		self.func = func
		self.args = args

	def run(self):
		apply(self.func,self.args)

def loop(nloop,nsec):
	print "loop",nloop," start at: ",ctime()
	sleep(nsec)
	print "loop",nloop,"end    at: ",ctime()

print "all start at: ",ctime()

loops = [4,2]
threads = []
nloops = range(len(loops))

for i in nloops:
	t = MyThread(loop,(i,loops[i]),loop.__name__)
	threads.append(t)

for i in nloops:
	threads[i].start()

for i in nloops:
	threads[i].join()

print "all end   at: ",ctime()
```

保存为threading_class_MyThread.py，运行，看一下结果。

![threading_class_MyThread.jpg](images/threading_class_MyThread.jpg)

#### 生产者-消费者模式

然后我们再来介绍一种多线程模式，生产者-消费者模式，这也是现实生活中最常用的多线程模式。
假设我们有这样一条工程，一共有两道工序。必须等到第一道工序结束了才能进行第二道工序。这时我们就引入了生产者和消费者的概念，第一道工序是生产者，第二道工序是消费者，分别是两个线程。
首先我们需要使用Queue队列模块，让多个线程之间共享数据。生产者不停的往队列里面加入货物，消费者不停的从队列里消费货物。
假设我们一共有100个货物，生产者与消费者所需时间都是1秒以内的随机时间。

```python
# coding=utf-8

import threading
from Queue import Queue
from random import random
from time import ctime,sleep

def writeQ(queue):
	for i in range(100):
		print "Producting project for Q..."
		sleep(random())
		# sleep(random()/2.0)
		queue.put('xxx',1)
		print "Size now",queue.qsize()

def readQ(queue):
	for i in range(100):
		print "Consuming project from Q..."
		sleep(random())
		queue.get(1)
		print "Size now",queue.qsize()

print "all start at: ",ctime()

funcs = [writeQ,readQ]
nfunc = range(len(funcs))

q = Queue(48)
threads = []

for i in nfunc:
	t = threading.Thread(target=funcs[i],args=(q,))
	threads.append(t)

for i in nfunc:
	threads[i].start()

for i in nfunc:
	threads[i].join()

print "all end   at: ",ctime()
```

保存为为threading_queue.py，运行，看一下结果。

###### 八个线程
最后总花费大概50秒左右，已经能够把效率提高一倍了。可是仅仅这样怎么够，这才两个线程，让我们来开八个线程试一下，生产者和消费者各四个线程。
果然在把生产者消费者线程增多的时候，相比较效率提高了很多。

```python
# coding=utf-8

import threading
from Queue import Queue
from random import random
from time import ctime,sleep

def writeQ(queue):
	for i in range(25):
		print "Producting project for Q..."
		sleep(random())
		queue.put('xxx',1)
		print "Size now",queue.qsize()

def readQ(queue):
	for i in range(25):
		print "Consuming project from Q..."
		sleep(random())
		queue.get(1)
		print "Size now",queue.qsize()

print "all start at: ",ctime()

funcs = [writeQ,readQ]
nfunc = range(len(funcs))

q = Queue(48)
threads = []

for i in nfunc:
	for j in range(4):
		t = threading.Thread(target=funcs[i],args=(q,))
		threads.append(t)

for i in range(8):
	threads[i].start()

for i in range(8):
	threads[i].join()

print "all end   at: ",ctime()
```

保存为threading_queue_last.py。
我们这是把生产者消费者同时执行，如果在生产者花费时间较短，只要时间在消费者的时候，我们可以先让生产者生产全部的货物，然后开多个子线程让消费者将其消费完为止。


#### 资源锁定
前面我们已经看到因为线程同步的原因，输出的时候总是显得不那么整齐，就是因为多线程在抢占同一个资源的原因。而如果我们在对同一个数据进行操作时，因为多线程的原因，可能一个线程对其进行操作还未结束另一个线程就强行进行了下一轮更改，这样的话肯定会有一些问题。
所以这就需要资源锁定，当一个资源被锁定的时候，同时只能有一个资源对其进行操作，这样就保证了多线程的安全性。

我们先来看一下没有资源锁的情况

```python
# coding=utf-8

import threading
from time import ctime,sleep

counter = 0

class MyThread1(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		global counter
		counter += 1
		print "  "+str(counter)+"  "

class MyThread2(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		global counter
		counter -= 1
		print "  "+str(counter)+"  "

if __name__ == '__main__':
	threads = []
	for i in range(20):
		if i%2:
			t = MyThread1()
		else:
			t = MyThread2()
		threads.append(t)

	for t in threads:
		t.start()
```

保存为Threading_nolock.py，运行，看一下结果。

![threading_nolock.jpg](images/threading_nolock.jpg)

现在我们将其上锁。

```python
# coding=utf-8

import threading
from time import ctime,sleep

counter = 0
lock = threading.Lock()

class MyThread1(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		if lock.acquire():
			global counter
			counter += 1
			print "  "+str(counter)+"  "
			lock.release()

class MyThread2(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		if lock.acquire():
			global counter
			counter -= 1
			print "  "+str(counter)+"  "
			lock.release()

if __name__ == '__main__':
	threads = []
	for i in range(20):
		if i%2:
			t = MyThread1()
		else:
			t = MyThread2()
		threads.append(t)

	for t in threads:
		t.start()
```

保存为threading_lock.py，运行，看一下结果。

![threading_lock.jpg](images/threading_lock.jpg)

使用线程锁的话需要手动的获取和释放，也可以采用简洁的方法,使用 上下文管理器。

```
def run(self):
	with lock:
		global counter
		counter -= 1
		print "  "+str(counter)+"  "
```

Lock 与 RLock 的区别，Lock 只能锁一次，再次请求就会挂起，RLock 自带计数器，在一个线程中可以请求多次，等计数器全部释放之后，其他线程才能取得资源。

#### 本地变量

threadLocal 线程局部变量，避免了使用全局变量需加锁的困境和局部变量调用不清的麻烦。保证在每个线程中的变量都是在线程内可读可写的，而不会被其他线程污染。

```
# -*- coding: utf-8 -*-

import threading


local = threading.local()


def process_name():
    print "hello %s, in %s" % (local.name, threading.current_thread().name)


def process_local(name):
    local.name = name
    process_name()


if __name__ == '__main__':
    local.name = 'Cli'
    process_name()
    t1 = threading.Thread(target=process_local, args=('Bob', ), name='Target-A')  # noqa
    t2 = threading.Thread(target=process_local, args=('Alice', ), name='Target-B')  # noqa

    t1.start()
    t2.start()

    t1.join()
    t2.join()

```

线程变量是只能在当前线程中使用，在 flask 中即当前请求。但是 flask 不仅仅是只支持多线程，还有多进程，甚至单线程。

如何在单线程中使每个请求都获得一份局部变量。
- 将局部变量变成实例属性。
