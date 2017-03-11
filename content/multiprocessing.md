## multiprocessing

基础的多进程库，可以进行一些简单的多进程操作

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
