##socket

socket网络编程，我其实一直是拒绝讲这个的，因为这个socket涉及到的知识面之广，我怕我个人也难以解释清楚。                                             

socket是一种基于TCP/IP协议的，在TCP/IP与应用层之间传输的网络通信方式。              
TCP/IP协议是一套使用使用广泛的通信协议的合集。                           
正如在全中国推行普通话一样，通信协议就是通信标准，不同的语言或者信息在同样的标准下可以相互传输并正常交流，这就是通信协议的功能。         

在这里我们就不再深入的研究TCP/IP协议，它包括很多的内容，具体的可以看一下：          
《TCP/IP协议详解》                              
[协议森林]()                    

这是一张标准的OSI七层模型中的底层协议图                        
![tcp.jpg](images/tcp.jpg)

可以看到图中除了TCP协议还有UDP协议，TCP协议需要经过三次握手才能建立持久稳定的连接，而UDP协议只管收发信息，并不会管是否接受。                             
TCP协议是持久的，有效的，可靠的。                       
UDP协议是快速的，简单的，少量的。                             

那么接下来让我们看一下socket在哪里呢。                        
![socket.jpg](images/socket.jpg)

socket抽象层是在TCP/IP协议之上的与应用层之间连接的抽象层，也就是说socket能够通过使用TCP协议或者UDP协议来实现很多相关的应用性协议功能的，比如说http，https，FTP，smtp，DNS等，或者是在两个或多个进程之间交流，传输数据。                             

网络通信之间都是至少需要一个服务器端和一个客户端的，我们的socket就先从简单的客户端开始。    

####简单的TCP协议的网络客户端              

```python
#coding=utf-8
import socket,sys

host = sys.argv[1]
port = sys.argv[2]

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))

while 1:
	buf = s.recv(2048)
	if not len(buf):
		break
	print buf
```

####简单的TCP协议的网络服务器

```python

```
