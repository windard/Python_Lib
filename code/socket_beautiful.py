#*-* coding:utf-8 *-*
import socket
import select
import sys
import signal
class ChatServer():
  def __init__(self,host,port,timeout=10,backlog=5):
    #记录连接的客户端数量
    self.clients =0
    #存储连接的客户端socket和地址对应的字典
    self.clientmap={}
    #存储连接的客户端socket
    self.outputs = []
    #建立socket
    self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    self.server.bind((host,port))
    self.server.listen(backlog)
    #增加信号处理
    signal.signal(signal.SIGINT,self.sighandler) 
  def sighandler(self):
    sys.stdout.write("Shutdown Server......\n")
    #向已经连接客户端发送关系信息，并主动关闭socket
    for output in self.outputs:
      output.send("Shutdown Server")
      output.close()
    #关闭listen
    self.server.close()
    sys.stdout.flush()
  #主函数，用来启动服务器
  def run(self):
    #需要监听的可读对象
    inputs=[self.server]
    
    runing=True
    #添加监听主循环
    while runing:
      try:
        readable,writeable,exceptional = select.select(inputs,self.outputs,[])
        #此处会被select模块阻塞，只有当监听的三个参数发生变化时，select才会返回
      except select.error,e:
        break
      #当返回的readable中含有本地socket的信息时，表示有客户端正在请求连接
      if self.server in readable:
        #接受客户端连接请求
        client,addr=self.server.accept()
        sys.stdout.write("New Connection from %s\n"%str(addr))
        sys.stdout.flush()
        #更新服务器上客户端连接情况
        #1，数量加1
        #2，self.outputs增加一列
        #3，self.clientmap增加一对
        #4, 给input添加可读监控
        self.clients += 1
        self.outputs.append(client)
        self.clientmap[client]=addr
        inputs.append(client)
      
      #readable中含有已经添加的客户端socket，并且可读
      #说明 1,客户端有数据发送过来或者 2,客户端请求关闭
      elif len(readable) != 0:
        #1, 取出这个列表中的socket
        csock=readable[0]
        #2, 根据这个socket，在事先存放的clientmap中，去除客户端的地址，端口的详细信息
        host,port = self.clientmap[csock]
        #3,取数据, 或接受关闭请求，并处理
        #注意，这个操作是阻塞的，但是由于数据是在本地缓存之后，所以速度会非常快
        try:
          data = csock.recv(1024).strip()
          for cs in self.outputs:
            if cs != csock:
              cs.send("%s\n"%data)
        except socket.error,e:
          self.clients -= 1
          inputs.remove(csock)
          self.outputs.remove(csock)
          del self.clientmap[csock]
      #print self.outputs
    self.server.close()
        
if __name__ == "__main__":
  chat=ChatServer("",8008)
  chat.run()