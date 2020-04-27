## getpass

这个库的功能很简单，也很有用，就是在输入的时候输入字符不回显出来。它只有两个函数，`getpass`和`getuser`,功能分别是输入不进行回显和获得当前系统登录用户名。

> getuser 有时候很有用，比如创建文件放到当前登陆用户的家目录下 `"/home/{}/".format(getpass.getuser())`,其实在 bash 中有这个环境变量 `$USER`。

```python

import getpass
#输入不回显，默认会提示password
pass1 = getpass.getpass()
#输入不回显，但是提示 请输入密码
pass2 = getpass.getpass("请输入密码:")
print pass1
print pass2
#登录系统的用户名
print getpass.getuser()
```

![getpass_demo.jpg](images/getpass_demo.jpg)
