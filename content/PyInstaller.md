##PyInstaller

将Python文件打包编译成exe文件Python库，除了py2exe比较常用之外，还有就是PyInstaller了，而且这个库的使用比py2exe更简单一些。

###安装

1. 下载pyinstaller并解压。[这里](http://nchc.dl.sourceforge.net/project/pyinstaller/2.0/pyinstaller-2.0.zip)是在sourceforge下载，或者在[这里](../others/pyinstaller-2.0.zip)下载。

2. 下载pywin32并解压安装。[这里](../others/pywin32-218.win32-py2.7.zip)下载解压安装。
>这是pyinstaller的一个依赖库，没有安装的话，在使用pyinstaller时会报错`Error: PyInstaller for Python 2.6+ on Windows needs pywin32.`

3. cmd中进入pyinstaller的解压之后的目录，因为pyinstaller并不需要安装，只需要解压就可以使用。在cmd中进入解压之后的目录，输入`python pyinstaller.py  `

如果有一下信息即表示可以正常使用了。

```bash
C:\Users\dell\Downloads\pyinstaller-2.0\pyinstaller-2.0>python pyinstaller.py
Usage: python pyinstaller.py [opts] <scriptname> [ <scriptname> ...] | <specfile>

pyinstaller.py: error: Requires at least one scriptname file or exactly one .spec-file
```

###一个简单的例子

```
#coding=utf-8
print "hello world"
```

保存为hello.py，在pyinstaller的解压之后的目录下。

在cmd中进入解压之后的目录，输入`python pyinstaller.py hello.py `

```bash
C:\Users\dell\Downloads\pyinstaller-2.0\pyinstaller-2.0>python pyinstaller.py hello.py
16 INFO: wrote C:\Users\dell\Downloads\pyinstaller-2.0\pyinstaller-2.0\hello\hello.spec
30 INFO: Testing for ability to set icons, version resources...
46 INFO: ... resource update available
46 INFO: UPX is not available.
940 INFO: checking Analysis
940 INFO: building Analysis because out00-Analysis.toc non existent
940 INFO: running Analysis out00-Analysis.toc
940 INFO: Adding Microsoft.VC90.CRT to dependent assemblies of final executable
2651 INFO: Searching for assembly x86_Microsoft.VC90.CRT_1fc8b3b9a1e18e3b_9.0.21022.8_none ...
2651 INFO: Found manifest C:\WINDOWS\WinSxS\Manifests\x86_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.21022.8_none_bcb86ed6ac711
2651 INFO: Searching for file msvcr90.dll
2651 INFO: Found file C:\WINDOWS\WinSxS\x86_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.21022.8_none_bcb86ed6ac711f91\msvcr90.dl
2651 INFO: Searching for file msvcp90.dll
2651 INFO: Found file C:\WINDOWS\WinSxS\x86_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.21022.8_none_bcb86ed6ac711f91\msvcp90.dl
2651 INFO: Searching for file msvcm90.dll
2665 INFO: Found file C:\WINDOWS\WinSxS\x86_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.21022.8_none_bcb86ed6ac711f91\msvcm90.dl
2776 INFO: Analyzing C:\Users\dell\Downloads\pyinstaller-2.0\pyinstaller-2.0\support\_pyi_bootstrap.py
3605 INFO: Analyzing C:\Users\dell\Downloads\pyinstaller-2.0\pyinstaller-2.0\PyInstaller\loader\archive.py
3684 INFO: Analyzing C:\Users\dell\Downloads\pyinstaller-2.0\pyinstaller-2.0\PyInstaller\loader\carchive.py
3809 INFO: Analyzing C:\Users\dell\Downloads\pyinstaller-2.0\pyinstaller-2.0\PyInstaller\loader\iu.py
3839 INFO: Analyzing hello.py
3839 INFO: Hidden import 'encodings' has been found otherwise
3839 INFO: Looking for run-time hooks
3839 INFO: Analyzing rthook C:\Users\dell\Downloads\pyinstaller-2.0\pyinstaller-2.0\support/rthooks/pyi_rth_encodings.py
4208 INFO: Warnings written to C:\Users\dell\Downloads\pyinstaller-2.0\pyinstaller-2.0\hello\build\pyi.win32\hello\warnhello
4224 INFO: checking PYZ
4224 INFO: rebuilding out00-PYZ.toc because out00-PYZ.pyz is missing
4224 INFO: building PYZ out00-PYZ.toc
4800 INFO: checking PKG
4800 INFO: rebuilding out00-PKG.toc because out00-PKG.pkg is missing
4800 INFO: building PKG out00-PKG.pkg
4816 INFO: checking EXE
4816 INFO: rebuilding out00-EXE.toc because hello.exe missing
4816 INFO: building EXE from out00-EXE.toc
4816 INFO: Appending archive to EXE C:\Users\dell\Downloads\pyinstaller-2.0\pyinstaller-2.0\hello\build\pyi.win32\hello\hell
4832 INFO: checking COLLECT
4832 INFO: building COLLECT out00-COLLECT.toc
```

然后就会在当前目录下生成一个hello的文件夹，进入文件夹，有两个文件，一个build，一个dist，在dist中即有编译好了的hello.exe文件。

###更详细的使用

参数说明：

```bash
-F, --onefile EXE只有一个文件

-D, --onedir EXE放在同一个目录中（默认是这个）

-K, --tk 包含TCL/TK

-d, --debug 生成debug模式的exe文件

-w, --windowed, --noconsole 窗体exe文件(Windows Only)

-c, --nowindowed, --console 控制台exe文件(Windows Only)

-o DIR, --out=DIR 设置spec文件输出的目录，默认在PyInstaller同目录

--icon=<FILE.ICO> 加入图标（Windows Only）

-v FILE, --version=FILE 加入版本信息文件

```

比如说我编译一个PyQt4的带ico的Python文件`python pyinstaller.py  -w  --onefile --icon="2048.ico" 2048.py`

###其他

注意一点，我在使用的时候，准备加入一个ico图标，结果出现下面的报错

```bash
    hsrc = win32api.LoadLibraryEx(srcpath, 0, LOAD_LIBRARY_AS_DATAFILE)
pywintypes.error: (193, 'LoadLibraryEx', '%1 \xb2\xbb\xca\xc7\xd3\xd0\xd0\xa7\xb5\xc4 Win32 \xd3\xa6\xd3\xc3\xb3\xcc\xd0\xf2
```

我在网上找到因为我的ico图标是jpg格式，需要转换格式为ico格式才可以，我把后缀名把jpg改为ico都不行。

发现这个打包编译的库比py2exe好使一些，py2exe虽然加入了ico，但是并不能够显示出来，但是这个就可以在所有的地方都显示出来。

我在使用py2exe的时候有一个地方也是报错。

```bash
Adding python27.dll as resource to C:\Users\dell\.ssh\PyQt_2048\dist\greedSnake.exe
```

总是卡在这里，后来才发现也是在使用ico格式的时候弄错了，还是不能使用jpg或是png格式的图片来代替ico



