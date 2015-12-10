##rarfile

与上面的用法基本一致，但是使用较少,就只写解压文件的代码吧。                    

```python
#coding=utf-8
import rarfile
g = rarfile.RarFile('demo.rar')
#解压到当前文件夹
g.extractall()
g.close()
```
