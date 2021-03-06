## pyscreenshot

看名字就知道这是一个截图用的库，在 Python 中，用来截图的库有很多，比如图像处理库 PIL 中的 ImageGrab , 或者是 GUI 的库中TK ， Qt 都有截图的函数，或者是 Windows 下的 win32 库也可以截图 ，而这个 pyscreenshot 是一个专门用来截图的库。

### PIL

```python


from PIL import ImageGrab

img = ImageGrab.grab()

# img = ImageGrab.grab((10,10,510,510))

img.save('grab_pil_demo.png','PNG')
```

### Qt4

```python


import sys  
from PyQt4.QtGui import QPixmap, QApplication  

app = QApplication(sys.argv)  
QPixmap.grabWindow(QApplication.desktop().winId()).save('grab_qt_demo.png', 'png')  
```

### Win32

```python


import Image
import win32gui, win32ui, win32con, win32api  

hwnd = 0 
hwndDC = win32gui.GetWindowDC(hwnd)   
mfcDC=win32ui.CreateDCFromHandle(hwndDC)   
saveDC=mfcDC.CreateCompatibleDC()   
saveBitMap = win32ui.CreateBitmap()   
MoniterDev=win32api.EnumDisplayMonitors(None,None)  

#print w,h　　　＃图片大小  
w = MoniterDev[0][2][2]  
h = MoniterDev[0][2][3]  
saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)   
saveDC.SelectObject(saveBitMap)   
saveDC.BitBlt((0,0),(w, h) , mfcDC, (0,0), win32con.SRCCOPY)  
bmpname = "grab_win32_demo.bmp"
saveBitMap.SaveBitmapFile(saveDC, bmpname)  
Image.open(bmpname).save(bmpname[:-4]+".png") 
```

```
# coding=utf-8
import win32gui
import win32ui
import win32con
import win32api

# 获取桌面
hdesktop = win32gui.GetDesktopWindow()

# 分辨率适应
width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

# 创建设备描述表
desktop_dc = win32gui.GetWindowDC(hdesktop)
img_dc = win32ui.CreateDCFromHandle(desktop_dc)

# 创建一个内存设备描述表
mem_dc = img_dc.CreateCompatibleDC()

# 创建位图对象
screenshot = win32ui.CreateBitmap()
screenshot.CreateCompatibleBitmap(img_dc, width, height)
mem_dc.SelectObject(screenshot)

# 截图至内存设备描述表
mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)

# 将截图保存到文件中
screenshot.SaveBitmapFile(mem_dc, 'grab_win32_second.bmp')

# 内存释放
mem_dc.DeleteDC()
win32gui.DeleteObject(screenshot.GetHandle())
```

### pyscreenshot

这个虽说是专门用来截图的库，但是它的底层也还是调用前面的几种的方式，只不过它将前面的几种调用方式都封装起来了，根据你电脑上的安装情况来自行调用。

不过也因为它是在内部是创建一个子进程调用其他的库，所以它就必须要有一个 __main__ 函数来开始。

函数 pyscreenshot.backends() 可以看到它支持这些底层库 ['pil', 'wx', 'pygtk', 'pyqt', 'scrot', 'imagemagick'] 。

#### 截全图

```python


import pyscreenshot

def main():
	# 截全屏
	im=pyscreenshot.grab()
	# 查看截屏图片
	# im.show()

	# 保存图片
	pyscreenshot.grab_to_file('grab_py_demo.png')
	
if __name__ == '__main__':
	main()

```

也可以这样

```
python -m pyscreenshot.examples.showgrabfullscreen
```

#### 截部分

```


import pyscreenshot

def main():
	# 截部分屏幕
	im=pyscreenshot.grab(bbox=(10,10,510,510)) 
	# 查看截屏图片
	# im.show()

	# 保存图片
	pyscreenshot.grab_to_file('grab_py_part.png')

if __name__ == '__main__':
	main()
```

也可以这样

```
python -m pyscreenshot.examples.showgrabbox
```