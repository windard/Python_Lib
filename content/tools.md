## Python 学习中用到的工具

### pip

安装 pip 最简单的方法还是下载 [get-pip.py](https://bootstrap.pypa.io/get-pip.py),然后运行，简单方便跨平台。

```
wget https://bootstrap.pypa.io/get-pip.py --no-check-certificate
```

然后可以使用 `-i http://pypi.douban.com/simple --trusted-host pypi.douban.com` 来为 pip 加速。

每次安装都手动填写 pip 的源确实不方便，可以修改 Mac/Linux 下的 `~/.pip/pip.conf` 或者 Windows 下的 `C:\Users\(username)\pip\pip.ini`  .

```
[global]
trusted-host =  pypi.douban.com
index-url = http://pypi.douban.com/simple
```

有一些库在 Windows 下可能不好安装，需要自行编译，可以下载别人已经编译好的可执行文件 whl 安装，Python 第三方库网站 [http://www.lfd.uci.edu/~gohlke/pythonlibs/](http://www.lfd.uci.edu/~gohlke/pythonlibs/) ，下载好之后 `pip install XXX.whl` 即可。

当一些库已经下载的时候，可以用 `--ignore-installed` 忽略已安装的库。

当一些依赖库其实不需要的时候，可以用 `--no-deps`, `--no-dependencies` 来忽略库中的依赖。


## virtualenv

创建虚拟环境

```
virtualenv venv
```

激活虚拟环境

Linux 下

```
source venv/bin/activate
```

Windows 下

```
venv/Scripts/activate
```

退出虚拟环境

```
deactivate 
```

创建指定版本的 Python

```
virtualenv -p /usr/bin/python2.7 venv
```

### ipython

最近使用了一个好东西，jupter notebook ，简单记录一下使用情况。

```
jupyter notebook 
jupyter notebook --no-browser
jupyter notebook --port 9999
jupyter notebook --help
jupyter notebook --ip=0.0.0.0 #外部访问

#常用：jupyter notebook --no-browser --port 5000 --ip=0.0.0.0
```

rich output

```
from IPython.display import HTML, Image, YouTubeVideo
from IPython.display import Image
Image(url='http://python.org/images/python-logo.gif')
```

### Anaconda

专业的科学计算发行版，自带各种科学计算的包，还有自带包管理功能和环境管理功能。

```
# 查看帮助
conda -h 

# 基于python3.6版本创建一个名字为python36的环境
conda create --name python36 python=3.6 

# 激活此环境
activate python36  
source activate python36 # linux/mac

# 再来检查python版本，显示是 3.6
python -V  

# 退出当前环境
deactivate python36 

# 删除该环境
conda remove -n python36 --all

# 或者 
conda env remove  -n python36

# 查看所以安装的环境
conda info -e
python36              *  D:\Programs\Anaconda3\envs\python36
root                     D:\Programs\Anaconda3
```

canda 的包管理功能

```
# 安装 matplotlib 
conda install matplotlib
# 查看已安装的包
conda list 
# 包更新
conda update matplotlib
# 删除包
conda remove matplotlib

# 更新conda本身
conda update conda
# 更新anaconda 应用
conda update anaconda
# 更新python，假设当前python环境是3.6.1，而最新版本是3.6.2，那么就会升级到3.6.2
conda update python
```

修改 conda 的镜像地址，可以采用[清华的 tuna 源](https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/)

```
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --set show_channel_urls yes
```

或者直接修改 `~/.condarc` (Linux/Mac) 或 `C:\Users\(username))\.condarc` (Windows) 

```
channels:
 - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
 - defaults
show_channel_urls: true
```

## Python 编码规范

Python 官方编码规范是 pep8, [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)

这里是中文版 [Python 风格指南](http://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/)

推荐使用 jetbrain 的 pycharm，自带 pep8 规范检测和改正，或者其他编辑器也需使用 pep8 编码规范插件。

感觉这个网站挺不错的,可以一看，[在线手册中心](http://docs.pythontab.com/)

[Python 2 在线手册](http://docs.pythontab.com/python/python2.7/)

[Python 3 在线手册](http://docs.pythontab.com/python/python3.5/)

[TensorFlow官方文档中文版](http://docs.pythontab.com/tensorflow/get_started/introduction/)
