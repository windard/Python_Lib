## twine

打包上传发布 python 库

在完成 `setup.py` 文件后

```
# coding=utf-8

from setuptools import setup

version = '0.1.1'

setup(
    name='my-bencoding',
    packages=['my_bencoding'],
    version=version,
    description='bencoding in python2 and python3, for code and study',
    author='Windard Yang',
    author_email='windard@qq.com',
    url='https://windard.com',
    python_requires='>=2.6',

    license="MIT",
    keywords='Bencoding In Python2 And Python3',

)

```

生成发布文件

```
python setup.py sdist bdist_wheel
```

发布到 pypi

```
twine upload dist/*
```

> 原始的发布命令是这样的 `python setup.py sdist upload`

或者是发布到其他地方

```
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

发布到 pypi 一般都需要先创建登录 pypi 的账户，可以创建 `~/.pypirc` 文件，填入账户信息

```
[distutils]
index-servers=
  pypi
  pypitest

[pypi]
repository = https://upload.pypi.org/legacy/
username = windard
password = xxx

[pypitest]
repository=https://test.pypi.org/legacy/
username = windard
password = xxx
```
