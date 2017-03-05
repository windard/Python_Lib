## opencv

有名的图像处理库，可以处理图像，视频，2D，3D 一切与图像有关的东西。opencv 也有和 Python 一样的问题，2.X 的版本与 3.X 的版本不兼容，虽然在使用的时候，导入 opencv 库的时候都叫 cv2 。但是并不是和其他的库一样 2.X 支持 python 2，3.X 支持 python 3 ，它的这俩版本都是支持 Python 2 的。。。

可以通过

```
>>> import cv2
>>> cv2.__version__
'3.0.0'
```

查看 openCV 的版本

### 安装使用

在 [官网](http://opencv.org/downloads.html) 下载 opencv 安装，其实安装就是一个解压的过程，然后将 `/opencv/build/python/cv2.pyd` 复制到 python 的 `/Python27/Lib/site-packages` 目录下即可使用。

在 `/opencv/sources/samples/python` 有一些 opencv 的示例源码，可以尝试运行一下，可能需要安装 numpy 库。

下面使用的 openCV 若未特殊强调，都是使用 `2.4.13` 的版本

### 图片处理

#### 打开图片

```
# coding=utf-8

import cv2   
  
img = cv2.imread("code.jpg")   
cv2.namedWindow("Image")   
cv2.imshow("Image", img)   
cv2.waitKey (0)
cv2.destroyAllWindows()  
```

### 视频处理

### 打开视频

```
import numpy as np
import cv2

cap = cv2.VideoCapture('vtest.avi')

while(cap.isOpened()):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### 打开摄像头

`s` 键保存图像，`q` 键退出 

```
# coding=utf-8

import cv2
import time

cap = cv2.VideoCapture(0)

while(True):
    # 每次从视频数据流框架中抓取一帧图片
    ret, frame = cap.read()

    # 将图片显示在特定窗口上
    cv2.imshow('OpenCV Capture',frame)

    # 当按下 q 键时退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # 当按下 s 键时保存图像
    key = cv2.waitKey(1)
    if key == ord('s'):
        filename = time.strftime('%Y%m%d-%H%M%S') + ".jpg"
        cv2.imwrite(filename, frame)
```

用 `openCV 3.0.0` 的话，是这样

```
coding=utf-8

import cv2.cv as cv

capture = cv.CaptureFromCAM(0)

# 定义一个无限循环
while 1:

  # 每次从视频数据流框架中抓取一帧图片
    image = cv.QueryFrame(capture)

    # 将图片显示在特定窗口上
    cv.ShowImage("OpenCV Capture", image)

    # 当按下Esc键时退出循环
    c = cv.WaitKey(1)
    if c == 27:
        break
```

### 录视频

其中最主要的函数为 `CreateVideoWriter`，`fourcc` 为编码格式，fps (frame per second) 每秒帧数

```
CreateVideoWriter(...)
    CreateVideoWriter(filename, fourcc, fps, frame_size [, is_color]) -> CvVideoWriter*
```

`fourcc` 可选的编码格式为 

```
CV_FOURCC('P','I','M','1') = MPEG-1 codec
CV_FOURCC('M','J','P','G') = motion-jpeg codec
CV_FOURCC('M', 'P', '4', '2') = MPEG-4.2 codec
CV_FOURCC('D', 'I', 'V', '3') = MPEG-4.3 codec
CV_FOURCC('D', 'I', 'V', 'X') = MPEG-4 codec
CV_FOURCC('U', '2', '6', '3') = H263 codec
CV_FOURCC('I', '2', '6', '3') = H263I codec
CV_FOURCC('F', 'L', 'V', '1') = FLV1 codec
```

一般当 fps 大于 24 时，人眼无法区分，这也是电影的播放率，当 fps 低于 10 时，人眼会觉得略卡顿。

```
# coding=utf-8

import cv2.cv as cv

capture = cv.CaptureFromCAM(0)
temp = cv.QueryFrame(capture)
writer = cv.CreateVideoWriter("output.avi", cv.CV_FOURCC("D", "I", "B", " "), 25, cv.GetSize(temp), 1)

count = 0
while count < 500:
    image = cv.QueryFrame(capture)
    cv.WriteFrame(writer, image)
    cv.ShowImage('Image_Window',image)
    cv.WaitKey(1)
    count += 1
```

这是以 25 fps 记录 500 帧的视频，即 25 秒，也可以自定义记录，手动按 `q` 停止。

```
# coding=utf-8

import cv2
import cv2.cv as cv

capture = cv.CaptureFromCAM(0)
temp = cv.QueryFrame(capture)
writer = cv.CreateVideoWriter("output.avi", cv.CV_FOURCC("M","J","P","G"), 25, cv.GetSize(temp), 1)

while 1:
    image = cv.QueryFrame(capture)
    cv.WriteFrame(writer, image)
    cv.ShowImage('Image_Window',image)
    cv.WaitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
```

