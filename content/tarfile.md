## tarfile

*.tgz与*.tar.gz是同种格式的文件，都是现有tar打包之后的文件压缩为gz文件格式。                
tarfile这个库也是和linux下的tar命令一样，功能丰富，不仅能打包，还能够压缩。    

```python
#coding=utf-8
import tarfile
allfile = []
#此处我们也使用之前zipfile的递归的方法
def getall(begindir):
	global allfile
	newpath = os.listdir(begindir)
	for i in newpath:
		currentpath = os.path.join(begindir,i)
		if os.path.isdir(currentpath):
			getall(currentpath)
		else:
			allfile.append(currentpath)
#创建一个tar.gz的压缩包
tar = tarfile.open('demo.tar.gz','w:gz')
for i in allfile:
	tar.add(i)
tar.close()
```

保存为tarfile_demo.py。            

可以看到这个库的用法与之前的zipfile库的用法非常相似，而且解压的过程也非常相近。     

```python
#coding=utf-8
import tarfile 
#解压到当前文件夹
g = tarfile.open('demo.tar.gz','r:gz')
#此处也可以直接用g.extractall()
for i in g.getnames():
	g.extract(i)
```

保存为tarfile_unzip.py。            
                           
确实是与tar的用法基本一致，只不过在tar中每一次打开文件的模式需要指定压缩格式。         
w或者是w:\* 只进行简单的压缩，w: 不压缩，w:gz 使用gzip压缩方式,w:bz2 使用bzip2压缩方式。      