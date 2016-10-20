## webbrowser

打开图形界面默认浏览器，唯一有用的函数就是 open 。

```
>>> import webbrowser
>>> webbrowser.browser
'C:\\Program Files (x86)\\Internet Explorer\\IEXPLORE.EXE'
>>> webbrowser.open("http://baidu.com")
True
>>> webbrowser.open_new("http://baidu.com")
True
>>> webbrowser.open_new_tab("http://baidu.com")
True
```

虽说写的浏览器是 IE ，但是打开的还是我的 chrome ，而且后面的三个函数的效果一模一样。