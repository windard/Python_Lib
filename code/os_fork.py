# coding=utf-8

import os

# pid = os.fork()

# if pid:
#     print "Child Pid : %s, Current Pid %s"%(pid,os.getpid())
# else:
#     print "I am the child,Current Pid %s"%(os.getpid())

def create_child():
    pid0=os.getpid()
    print '主进程',pid0

    try:
        pid1=os.fork()
    except OSError:
        print u'你的系统不支持fork'
        exit()

    if pid1 <0:
        print u'创建子进程失败'
    elif pid1==0:
        print '这是在子进程里，看不到子进程的 pid:%d，因为那就是自己的 pid: %d，父进程就是主进程: %d '%(pid1,os.getpid(),os.getppid())
    else:
        print '这是在主进程里，可以看到子进程的 pid:%d ，和自己的进程:%d ,父进程也是其他的进程: %d '%(pid1,os.getpid(),os.getppid())

    print '这句话,父进程和子进程都会执行'

# create_child()
