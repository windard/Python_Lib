##media
原本以为media是一个很简单的图像处理库，结果下载就纠结我一半天。它不是Python自带的库，需要自行安装，而安装这个库又需要先安装一些其他的东西。本人环境Windows 10 64位处理器Python2.7.10。      
1. 下载[Python Imaging Library 1.1.7 for Python 2.7](../others/PIL-1.1.7.win32-py2.7.exe)，安装。    
2. 下载[pygame-1.9.1.win32-py2.7.msi](../others/pygame-1.9.1.win32-py2.7.msi)，安装。    
3. 下载[numpy-1.6.1-win32-superpack-python2.7.exe](../others/numpy-1.6.1-win32-superpack-python2.7.exe)，安装。    
4. 下载[gwpy-code.zip](../others/gwpy-code.zip)，解压，进入code->install，双击`PyGraphics-2.0.win32.exe`安装。     
>此处，本人安装的时候提示缺少了`MSVCR71.dll`，下载[msvcr71.rar](../others/msvcr71.rar)，安装。    
5. 下载[setuptools-0.6c11.win32-py2.7.exe](../others/setuptools-0.6c11.win32-py2.7.exe)    
6. 最后打开cmd，在命令行中输入`C:\Python27\Scripts\easy_install nose `，当然你得先安装了`ease_install`。   
7. 在cmd中使用`pip install media`即可。   

还有另一种比较简便的方法，全程使用pip安装。   

```
pip install Ampy  
pip install PyGraphics  
pip install nose  
pip install media    
```

####基本使用
算了，大家还是放弃这个库吧。安装非常复杂，使用起来也有问题。     