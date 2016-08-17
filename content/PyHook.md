## PyHook

这是用来监听键盘和鼠标的钩子，因为它是依赖于 PyWin32 的，因此只能在 Windows 上运行。

想要监听键盘或鼠标的事件，首先需要有一个 Windows 的消息通道，通过 PyWin32 扩展包的 pythoncom 来提供消息引入。