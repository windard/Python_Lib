##os

非常基础的一个库，但是却实现了我一个想了很久了功能，识别目录下的所有文件。

1. 取得当前目录--os.getcwd()
5. 更改当前目录——os.chdir()
2. 创建一个目录--os.mkdir()
3. 创建多级目录--os.makedirs()
4. 删除一个目录,只能删除空目录--os.rmdir("path")
5. 删除多个目录,删除目录及其下内容--os.removedirs（"path）
1. 获取目录中的文件及子目录的列表——os.listdir("path")		隐藏文件也会显示出来
3. 删除一个文件--os.remove()
4. 文件或者文件夹重命名--os.rename(old， new)
6. 获取文件大小--os.path.getsize（filename）
7. 获取文件属性--os.stat(file)
8. 修改文件权限与时间戳--os.chmod(file)
9. 路径中加入新的内容--os.path.join(path,file)
6. 将路径分解为目录名和文件名——os.path.split()
7. 将目录分解为目录加文件名和文件名的扩展名——os.path.splitext()
7. 获得路径的路径名--os.path.dirname()
8. 获得路径的文件名--os.path.basename()
8. 判断一个路径是否存在或是否为路径——os.path.isdir("path")
9. 判断一个文件是否存在或这否为文件——os.path.isfile("file")
10. 判断一个路径（目录或文件）是否存在——os.path.exists()
11. 判断一个路径是否是绝对路径--os.path.isabs()
9. 读取和设置环境变量--os.getenv() 与os.putenv()
10. 指示你正在使用的平台--os.name       对于Windows，它是'nt'，而对于Linux/Unix用户，它是'posix'
11. 给出当前平台使用的行终止符--os.linesep()    Windows使用'\r\n',Linux使用'\n',而Mac使用'\r'
12. 运行shell命令-- os.system()  
 >但是这个执行命令行没有返回值，直接输出，不管你有没有print                            
13. 执行shell命令-- os.popen() 
>执行命令行，返回一个file open的对象，需要read才能得到执行结果，但是还是没有返回值，如果需要更多的命令行操作，可以使用commands库
13. 终止当前进程--os._exit(0)      
14. 循环遍历目录--os.walk()  返回一个三元组，第一个是路径，第二个是路径下的目录，第三个是路径下的非目录。

```python
#coding=utf-8
import os

currentpath = os.getcwd()
print currentpath
changedpath = 'C:\\Users\\dell\\Desktop' 
os.chdir(changedpath)
currentpath = os.getcwd()
print currentpath
os.mkdir('hello')
changedpath = changedpath + '\\hello'
print changedpath
os.chdir(changedpath)
currentpath = os.getcwd()
print currentpath
os.makedirs('hello\\hello')
changedpath = changedpath + '\\hello\\hello'
print changedpath
os.chdir(changedpath)
currentpath = os.getcwd()
print currentpath
os.chdir('../')
currentpath = os.getcwd()
print currentpath
currentlist = os.listdir(currentpath)
print currentlist
os.rmdir('hello')
currentlist = os.listdir(currentpath)
print currentlist
os.chdir('../../')
currentpath = os.getcwd()
currentlist = os.listdir(currentpath)
print currentlist
os.removedirs('hello\\hello')
currentlist = os.listdir(currentpath)
print currentlist
FILE1 = open('test1.txt','w')
FILE1.close()
FILE2 = open('test2.txt','w')
FILE2.close()
currentlist = os.listdir(currentpath)
print currentlist
os.remove('test1.txt')
currentlist = os.listdir(currentpath)
print currentlist
os.rename('test2.txt','newtest.txt')
currentlist = os.listdir(currentpath)
print currentlist
FILE = open('newtest.txt','w')
FILE.write('THis is for test')
FILE.close()
FILESIZE = os.path.getsize('newtest.txt')
print FILESIZE
FILESTAT = os.stat('newtest.txt')
print FILESTAT
currentpath = currentpath + "\\newtest.txt"
print currentpath
(splitpath,splitfile) = os.path.split(currentpath)
print splitpath
print splitfile
(splitpath,splitfile) = os.path.splitext(currentpath)
print splitpath
print splitfile
splitpath = os.path.dirname(currentpath)
splitfile = os.path.basename(currentpath)
print splitpath
print splitfile
isdir = os.path.isfile(currentpath)
isfile = os.path.isdir(currentpath)
print isdir
print isfile
os.remove('newtest.txt')
currentpath = os.path.dirname(currentpath)
isdir = os.path.isfile(currentpath)
isfile = os.path.isdir(currentpath)
print isdir
print isfile
isexist = os.path.exists(currentpath)
print isexist
isabs = os.path.isabs(currentpath)
print isabs
osname = os.name
print osname
linesep = os.linesep
print linesep
os.system('dir')
```
保存为os_improve.py

保存为os_demo.py，运行，看一下结果             
![os_demo](images/os_demo.jpg)              
重点是还可以运行shell命令。          
```python
import os
shell = "dir"
print os.system(shell)
```
保存为os_shell.py，运行，看一下结果。            
![os_shell.jpg](images/os_shell.jpg)                  
试一下用`os.walk()`来遍历文件。              
```python
import os

dirlist = r"C:\Users\dell\Desktop\2048"
filenum = 0
dirnum  = 0
for i,j,k in os.walk(dirlist):
	print i
for i,j,k in os.walk(dirlist):
	for item in k:
		print item
	filenum = filenum + 1
	for index in range(len(k)):
		dirnum = dirnum + 1

print filenum
print dirnum
```
保存为os_walk.py，运行，看一下结果。               
![os_walk.jpg](images/os_walk.jpg)      

给一个查看目录下的所有文件的代码，如果有目录则空格表示递进关系         
```python
import os

def showall(path,leavel=0,filenum=0,show=True):
	newnum = filenum
	currentpath = path;
	dirandfile = os.listdir(path)
	for item in dirandfile:
		newpath = os.path.join(currentpath,item)
		if os.path.isdir(newpath):
			num = showall(newpath,leavel+1,newnum,show)
			newnum = num
		else:
			newnum = newnum + 1
			tab_stop = ""
			if show:
				for tab in range(leavel):
					tab_stop = tab_stop + " "
			print tab_stop + newpath

	return newnum

if __name__ == '__main__':
	num = showall('./',show=False)
	print "File Number : " + str(num)

```