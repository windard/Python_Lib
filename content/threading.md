##threading

在thread的库里还需要我们自己的去设定锁，并且在主线程里阻塞主线程的进行来判断锁是否已经释放。但是在threading库里，因为守护线程的存在，主线程会自动等待子线程全部结束才会继续下去，不过在这里还是需要手动的将子线程加入(join)到主线程中。               
还是上一个例子，我们用threading来试一下。                     
```python
#coding=utf-8
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


然后我们再来介绍一种多线程模式，生产者-消费者模式，这也是现实生活中最常用的多线程模式。   
假设我们有这样一条工程，一共有两道工序。必须等到第一道工序结束了才能进行第二道工序。这时我们就引入了生产者和消费者的概念，第一道工序是生产者，第二道工序是消费者，分别是两个线程。  
首先我们需要使用Queue队列模块，让多个线程之间共享数据。生产者不停的往队列里面加入货物，消费者不停的从队列里消费货物。
假设我们一共有100个货物，生产者与消费者所需时间都是1秒以内的随机时间。                 
```python
#coding=utf-8
import threading
from Queue import Queue
from random import random
from time import ctime,sleep
def writeQ(queue):
	for i in range(100):
		print "Producting project for Q..."
		sleep(random())
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

                     
最后总花费大概50秒左右，已经能够把效率提高一倍了。可是仅仅这样怎么够，这才两个线程，让我们来开八个线程试一下，生产者和消费者各四个线程。                         
果然在把生产者消费者线程增多的时候，相比较效率提高了很多。               
```python
#coding=utf-8
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

