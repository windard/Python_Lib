##这是一些用Python写的小项目。          

1. PortScan             
端口扫描器                      
项目地址：[PortScan](https://github.com/1106911190/Port_Scan)           

2. MailClient            
邮箱客户端，可以进行收发邮件的功能                
项目地址：[MailClient](https://github.com/1106911190/MailClient)          

3. FileList             
文件扫描器，可以查看相关目录下的文件和文件夹的情况。              
 - 用递归来写的             
  **Version：1.0**                   
  参数如下：                 
  1. `-o`可选参数，是否开启缩进，默认不开启。若开启，层次缩进四个空格。
  2. `-d`可选参数，是否扫描文件夹，默认扫描文件。若开启，则扫描文件夹，不扫描文件。
  >文件路径为绝对路径，扫描文件夹不包括源文件夹。
  3. `[begin]`必选参数，扫描的源文件夹。
  4. `--save=`可选参数，存储位置。默认在屏幕上打印出来，若保存到文本中，则为保存的文件名。

 - 用os.walk()写的                 
  **Version：1.0**
  参数如下：            
  1. `-d`可选参数，是否扫描文件夹，默认扫描文件。若开启，则扫描文件夹，不扫描文件。
  >文件路径仅为文件名，扫描文件夹包括源文件夹。
  2. `[begin]`必选参数，扫描的源文件夹。
  3. `--save=`可选参数，存储位置。默认在屏幕上打印出来，若保存到文本中，则为保存的文件名。

4. FileFinder
文件查找器，可以查找相关目录下的是否有相关文件。
 - 用递归来写的             
  **Version：1.0**                
  参数如下：              
  1. `[begin]`必选参数，源文件夹。
  2. `[filename]`必选参数，查找的关键词。
  >查找的也包括文件夹，得出的查询结果里也包含文件夹路径
 - 用os.walk()写的              
  **Version：1.0**
  参数如下：
  1. `[begin]`必选参数，源文件夹。
  2. `[filename]`必选参数，查找的关键词。
  >仅查找文件名，得出的查询结果仅包含所有的文件名

5. DecodeAndEncode 
加密与解密          
**Version:1.0**              
参数如下：                  
 1. `-d` 可选参数，使用加密算法
 2. `-e` 可选参数，使用解密算法
 3. `-f` 可选参数，计算文件的md5值或者sha1值
 4. `--type=[decode:(base64/base32/base16/md5/sha1),encode:(base64/base32/base16/ord),file:(md5/sha1)]` 必选参数，选择相应的加密或解密算法
 5. `--data=` 必选参数，加密或解密的字符串
 6. `--filename=` 课选参数，计算文件的hash值的文件（在cmd的936代码页下可以操作中文名的文件）
 7. `--save=` 可选参数，若保存到文本中，则保存的文件名

**Version:1.1**                  
增加对AES，DES，DES3，RSA加密算法的支持。

6. SocketChatroom        
内网聊天工具，可以在虚拟机或是在内网内实现简单的聊天室功能          
**Version:1.0**              
参数如下：          
1. `--type` 可选参数，实现的功能，默认为`client`，取值范围`server|client`          
2. `--host` 可选参数，服务器ip，默认为`127.0.0.1`           
3. `--port` 可选参数，服务器端口号，默认为`8888`           
4. `--name` 可选参数，聊天时使用的姓名                    

7. RSSReader
RSS阅读器，在每天早晚检查指定网站是否有更新，如果有即将最新更新以邮件形式发给我                     
需配合脚本与crontab使用                    
脚本如下：
```bash
echo "Starting Script">>/home/windard/Document/feed/feed.log
sudo service mysql start
echo "Starting MySQL">>/home/windard/Document/feed/feed.log
python /home/windard/Document/feed/feed.py
sudo service mysql stop
echo "Ending MySQL">>/home/windard/Document/feed/feed.log
echo "Ending Script">>/home/windard/Document/feed/feed.log
```
开启crontab                 
`sudo vim /ect/crontab`         
在最后一行加入                
`0 9,21    * * *     root    bash /home/windard/Document/feed/init.sh`

