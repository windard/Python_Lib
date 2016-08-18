## subprocess

这是一个函数执行的库，类似与 os.system , os.popen , commands 等命令执行的语句或库。

这个库中就只有一个类 Popen

```
class Popen(args, bufsize=0, executable=None,
            stdin=None, stdout=None, stderr=None,
            preexec_fn=None, close_fds=False, shell=False,
            cwd=None, env=None, universal_newlines=False,
            startupinfo=None, creationflags=0):
```

|参数 					|含义																									|
|-----					|----																									|
|agrs					|需要被执行的字符串或数组																				|
|bufsize 				|0 无缓冲，1 有缓冲，其他正值 缓冲区大小，负值 采用默认系统缓冲(一般是全缓冲)							|
|executable 			|一般不用吧，args字符串或列表第一项表示程序名 															|
|stdin，stdout，stderr	|None 没有任何重定向，继承父进程，PIPE 创建管道，文件对象，文件描述符(整数)，stderr 还可以设置为 STDOUT	|
|preexec_fn 			|钩子函数， 在fork和exec之间执行。(unix) 																|
|close_fds				|unix 下执行新进程前是否关闭0/1/2之外的文件，windows下不继承还是继承父进程的文件描述符 					|
|shell 					|为真的话，unix下相当于args前面添加了 "/bin/sh“ ”-c”，window下，相当于添加"cmd.exe /c"					|
|cwd 					|设置工作目录																							|
|env 					|设置环境变量 																							|
|universal_newlines 	|各种换行符统一处理成 '\n' 																				|
|startupinfo 			|window下传递给CreateProcess的结构体 																	|
|creationflags 			|windows下，传递CREATE_NEW_CONSOLE创建自己的控制台窗口													|

这个库有三个方法 call() , check_call() , check_output() ，其实也是在调用上面的那个类。

call() 执行程序，并等待它完成

```
def call(*popenargs, **kwargs):
    return Popen(*popenargs, **kwargs).wait()
```

check_call() 调用前面的call，如果返回值非零，则抛出异常

```
def check_call(*popenargs, **kwargs):
    retcode = call(*popenargs, **kwargs)
    if retcode:
        cmd = kwargs.get("args")
        raise CalledProcessError(retcode, cmd)
    return 0

```

check_output() 执行程序，并返回其标准输出

```
def check_output(*popenargs, **kwargs):
    process = Popen(*popenargs, stdout=PIPE, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        raise CalledProcessError(retcode, cmd, output=output)
    return output
```

