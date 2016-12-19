## pyftpdlib

python 中有一个 ftplib 库，用来做 FTP 客户端的，那么既然有客户端，肯定少不了服务器端， pyftpdlib 就是用来做 FTP 服务器端的。

可以方便快速的开启 FTP 服务。

```
λ python -m pyftpdlib
[I 2016-12-19 11:50:50] >>> starting FTP server on 0.0.0.0:2121, pid=14996 <<<
[I 2016-12-19 11:50:50] concurrency model: async
[I 2016-12-19 11:50:50] masquerade (NAT) address: None
[I 2016-12-19 11:50:50] passive ports: None
```

这种情况下默认是可以使用匿名身份（anonymous）登录，密码随意输入，而且拥有所有读写权限，所以短时期紧急情况下可用，想做稳定的 FTP 服务器的话，慎用。

那来开始正式的创建一个 FTP 服务器。

身份认证部分 

```
from pyftpdlib.authorizers import DummyAuthorizer

authorizer = DummyAuthorizer()
authorizer.add_user("user", "12345", "/home/giampaolo", perm="elradfmw")
authorizer.add_anonymous("/home/nobody")
```

add_user 函数原型如下:

```
add_user(username, password, homedir, perm='elr', msg_login='Login successful.', msg_quit='Goodbye.')
```

- username  : 登陆用户名
- password  : 登陆密码
- homedir   : 登陆之后根目录
- perm 	    : permission ，用户权限
- msg_login : 登陆成功时的返回消息
- msg_quit  : 登出时的返回消息

其中 permission 表包括 读 权限表和 写 权限表

```
|Read permissions:
| - "e" = change directory (CWD command)  									# 更改目录
| - "l" = list files (LIST, NLST, STAT, MLSD, MLST, SIZE, MDTM commands)    # 列举文件
| - "r" = retrieve file from the server (RETR command) 						# 获取文件
|
|Write permissions:
| - "a" = append data to an existing file (APPE command) 					# 文件写入
| - "d" = delete file or directory (DELE, RMD commands) 					# 删除文件或文件夹
| - "f" = rename file or directory (RNFR, RNTO commands) 					# 重命名文件或文件夹
| - "m" = create directory (MKD command) 									# 创建文件夹
| - "w" = store a file to the server (STOR, STOU commands)   				# 上传文件
| - "M" = change file mode (SITE CHMOD command) 							# 更改文件权限
```

add_anonymous 的函数原型如下：

```
add_anonymous(self, homedir, **kwargs)
```

参数基本与 add_user 一致。

一个简单的例子，因为我是在 Windows 上，所以就选用 D 盘和 E 盘作为根目录好了

```
# coding=utf-8

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

authorizer = DummyAuthorizer()
authorizer.add_user("admin", "password", "D:\\", perm="elradfmw")
authorizer.add_anonymous("E:\\", perm='elr')

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer(("127.0.0.1", 21), handler)
server.serve_forever()
```
