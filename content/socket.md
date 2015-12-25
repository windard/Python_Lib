##socket

socket网络编程，我其实一直是拒绝讲这个的，因为这个socket涉及到的知识面之广，我怕我个人也难以解释清楚。                                             

socket是一种基于TCP/IP协议的，在传输层与应用层之间进行信息交流的网络通信方式，它主要用于在同一台主机或不同的主机的进程之间的通信。              
TCP/IP协议是一套使用使用广泛的通信协议的合集。                           
正如在全中国推行普通话一样，通信协议就是通信标准，不同的语言或者信息在同样的标准下可以相互传输并正常交流，这就是通信协议的功能。         

在这里我们就不再深入的研究TCP/IP协议，它包括很多的内容，具体的可以看一下：          
《TCP/IP协议详解》                              
[协议森林](http://www.cnblogs.com/vamei/archive/2012/12/05/2802811.html)                    

这是一张TCP/IP参考模型图。                        
![tcp.jpg](images/tcp.jpg)

可以看到图中除了TCP协议还有UDP协议。        
TCP协议需要经过三次握手才能建立持久稳定的连接，而UDP协议只管收发信息，并不会管是否接受。                             
TCP协议是持久的，有效的，可靠的。                       
UDP协议是快速的，简单的，少量的。                             
socket对TCP和UDP都支持。                              

那么接下来让我们看一下socket在哪里呢。                        
![socket.jpg](images/socket.jpg)

socket抽象层是在TCP与UDP协议的运输层之上的与应用层连接的抽象层，也就是说socket能够通过使用TCP协议或者UDP协议来实现很多相关的应用性协议功能的，比如说http，https，FTP，smtp，DNS等。                             

网络通信之间都是至少需要一个服务器端和一个客户端的，我们的socket就先从简单的客户端开始。    

####简单的TCP协议的网络客户端              

```python
#coding=utf-8
import socket,sys

host = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
	s.connect((host,port))
	print "Connect Successful" 
except:
	print "Connect Failed"

s.send("hello server")

buf = s.recv(1024)
print "Received From Sercer : " + buf
```

保存为socket_client.py，运行，看一下结果。                   
![socket_client.jpg](images/socket_client.png)                 
可以看到，我先是在本机开了一个ftp服务器，用socket可以成功连接上去，然后就是连接百度的http服务器，看到也连接成功了，最后一个是连接后面的socket服务器，同样的返回了服务器的回复。可是为什么百度的http服务器没有回复呢？因为我们向它发送的请求不对,如果想要得到返回数据，我们需要发送一个GET请求,`GET / \HTTP1.1\r\n\r\n`。              

####简单的TCP协议的网络服务器

```python
#coding=utf-8
import socket

host = "127.0.0.1"
port = 8081

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))
s.listen(5)

print "Server is running on port %s Press Ctrl-C to stop"%port

while 1:
	clientsock,clientaddr = s.accept()
	print "Welcome from %s : %s"%(clientaddr[0],clientaddr[1])
	resquest = clientsock.recv(1024)
	print "Received From client : " + resquest
	clientsock.send("Hello client")
	clientsock.close()

s.close()
```

保存为socket_server.py，运行，看一下结果。                  
![socket_server](images/socket_server.png)                         
![socket_server_client](images/socket_server_client.png)                         

以上就是我们的socket的一个简单的使用了，接下来我们详细的讲解一下socket客户端和服务器端的相应的功能。                         

####建立一个socket客户端
1. 创建socket对象                           
`socketobject = socket.socket(family[,type])`                 
family有`AF_INET`包括internet地址，`AF_INET6`包括ipv6的internet地址，`AF_UNIX`同一台机器上。                    
type有`SOCK_STREAM`数据流套接字，`SOCK_DGRAM`数据报套接字，`SOCK_RAW`原始套接字。                  

2. 根据主机和端口找到socket并连接
`socketobject.connect((host,port))`
host和port构成一个元组。                      

3. 发送和接收数据
`socketobject.recv()`和`socketobject.send()`接收和发送数据。                   

####建立一个socket服务器
1. 创建一个socket对象
`socketcobject = socket.socket(family[[,type])`

2. 将socket绑定到一个指定端口上
`socketobject.bind((host,port))`
host和port构成一个元组，如果host为`0.0.0.0`或者为空时表示其可以接受所有ip的连接,如果port为0,即表示动态的选择一个端口。                 

3. 设置socket监听数目
`socketobject.listen(number)`number大于0,如果同时有多个客户端连接，即进入队列，若队列已满，则拒绝进入。                  

4. 连接客户端
`client = socketobject.accept()`client是一个socket对象和socket信息的元组。

5. 发送和接收数据
`clientobject.recv()`和`clientobject.send()`接收和发送数据。                         
发送数据还可以用`clientobject.sendall()`

6. 关闭客户端连接
`clientobject.close()`

7. 关闭socket服务器端
`socketobject.close()`

####socketobject的其他函数
1. socketobject.settimeout() 
2. socketobject.gettimeout()
3. socketobject.getpeername()
4. socketobject.getsocketname()
5. socketobject.getsocketoption()

```python
#coding=utf-8
import socket,sys

host = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
	s.connect((host,port))
	print "Connect Successful" 
except:
	print "Connect Failed"

s.send("hello server")

timeout = s.gettimeout()
print timeout

s.settimeout(2)

timeout = s.gettimeout()
print timeout

buf = s.recv(1024)
print "Received From Sercer : " + buf
```

保存为socket_client_improve.py，运行，看一下结果。                       
![socket_client_improve.png](images/socket_client_improve.png)

####socket的其他功能函数
1. socket.gethostname() 
2. socket.gethostbyname(host) 
3. socket.gethostbyaddr(host) 
4. socket.getservbyname(servicename[,protocolname]) 
5. socket.getprotobyname(name) 
6. socket.getservbyport(port[,protocolname])
7. socket.getaddrinfo(host,port[,family])
8. socket.setdefaulttimeout()
9. socket.getdefaulttimeout()
10. socket.ssl()

```python
#coding=utf-8

import socket

hostname = socket.gethostname()
print "host name : " + hostname

hostip = socket.gethostbyname(hostname)
print "host ip : " + hostip

host = socket.gethostbyaddr(hostip)
for item in host:
	print item

httpport = socket.getservbyname("http")
print "http port : " + str(httpport)

ftpport = socket.getservbyname("ftp","tcp")
print "tcp port : " + str(ftpport)

udpnumber = socket.getprotobyname("udp")
print "udp number is : " + str(udpnumber)

tcpnumber = socket.getprotobyname("tcp")
print "tcp number is : " + str(tcpnumber)

servivename = socket.getservbyport(25)
print "25 port is : " + servivename

servivename = socket.getservbyport(43)
print "43 port is : " + servivename

addrinfo = socket.getaddrinfo("www.baidu.com",None)
for item in addrinfo:
	print "www.baidu.com ip is : " + item[4][0]
```

保存为socket_get.py，运行，看一下结果。                       
![socket_get](images/socket_get.png)                 

####可复用的服务器端
我们现在的服务器端虽然是可以监听多个客户端连接，但是如果有一个客户端已经连接上却长时间占据着不结束的话，就会阻塞后面客户端的连接。            

所以为了可复用的服务器端，我们想到可以用多线程，来避免客户端阻塞。

```python
#coding=utf-8

import socket
import thread 

host = "127.0.0.1"
port = 8081

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))
s.listen(5)

def connect(clientsock,clientaddr):
	print "Welcome from %s : %s"%(clientaddr[0],clientaddr[1])
	clientsock.send("Hello client \n")
	while 1:
		resquest = clientsock.recv(1024)		
		while not len(resquest):
			break
		print "Received From No.%s client : "%clientaddr[1] + resquest,

print "Server is running on port %s Press Ctrl-C to stop"%port

while 1:
	clientsock,clientaddr = s.accept()
	thread.start_new_thread(connect ,(clientsock,clientaddr))

s.close()
```

保存为socket_server_thread.py，运行，看一下结果。                     

现在可以通过多个telnet来与服务器端相连接了，但是这里有一个新的问题，每一次当关闭服务器端之后，再次打开的时候就会报出端口已被占的错误。        
![socket_error.png](socket_error.png)                       

我们可以通过可重用套接字来解决这个问题。           

```python
#coding=utf-8

import socket
import thread 

def connect(clientsock,clientaddr):
	print "Welcome from %s : %s"%(clientaddr[0],clientaddr[1])
	clientsock.send("Hello client \n")
	while 1:
		resquest = clientsock.recv(1024)		
		while not len(resquest):
			break
		print "Received From No.%s client : "%clientaddr[1] + resquest,


host = "127.0.0.1"
port = 8081

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

old_state = s.getsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR)
print "Old State is : " + str(old_state)

s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
new_state = s.getsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR)
print "New State is : " + str(new_state)

s.bind((host,port))
s.listen(5)

print "Server is running on port %s Press Ctrl-C to stop"%port

while 1:
	clientsock,clientaddr = s.accept()
	thread.start_new_thread(connect ,(clientsock,clientaddr))

s.close()
```

保存为socket_server_sockopt.py，运行，看一下结果。               
![socket_server_sockopt.png](images/socket_server_sockopt.png)


