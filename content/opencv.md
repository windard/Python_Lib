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

# 打开并读取图片
img = cv2.imread("code.jpg")

# 为显示界面导航栏命名   
cv2.namedWindow("Image")

# 显示图片   
cv2.imshow("Image", img)

# 等待键盘输入   
key = cv2.waitKey(0)

# 按 q 键则直接退出
if key == 27:
    cv2.destroyAllWindows()
# 按 s 键则保存退出
elif key == ord('s'):
    cv2.imwrite("code.png", img)
    cv2.destroyAllWindows()
```

还可以使用 matplotlib 显示图片

```
# coding=utf-8

import cv2
from matplotlib import pyplot as plt

img = cv2.imread("code.jpg", cv2.IMREAD_COLOR)

plt.imshow(img)
plt.show()
```

但是在 openCV 中三原色的显示是 BGR 顺序，而 matplotlib 是 RGB 顺序，所以在显示中颜色会有一些差异，我们需要调整一下颜色。

```
# coding=utf-8

import numpy as np
import cv2
from matplotlib import pyplot as plt

img=cv2.imread('lena.png',cv2.IMREAD_COLOR)

#method1
b,g,r=cv2.split(img)
img2=cv2.merge([r,g,b])
plt.imshow(img2)
plt.show()

#method2
img3=img[:,:,::-1]
plt.imshow(img3)
plt.show()

#method3
img4=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img4)
plt.show()
```

### 视频处理

### 打开视频

不知为何，使用 openCV 打开视频的颜色都不对，还会视频对半分开错位。

```
import numpy as np
import cv2

cap = cv2.VideoCapture('vtest.avi')

while(cap.isOpened()):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('Video frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

```
# coding=utf-8

import cv2.cv as cv

capture = cv.CaptureFromFile('output.avi')

nbFrames = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_COUNT))

#CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream
#CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream

fps = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FPS)

wait = int(1/fps * 1000/1)

duration = (nbFrames * fps) / 1000

print 'Num. Frames = ', nbFrames
print 'Frame Rate = ', fps, 'fps'
print 'Duration = ', duration, 'sec'

for f in xrange( nbFrames ):
    frameImg = cv.QueryFrame(capture)
    print cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_POS_FRAMES)
    cv.ShowImage("The Video", frameImg)
    cv.WaitKey(wait)

```

```
# coding=utf-8

import cv2

#获得视频的格式
videoCapture = cv2.VideoCapture('output.avi')

#获得码率及尺寸
fps = videoCapture.get(cv2.cv.CV_CAP_PROP_FPS)
size = (int(videoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)), 
        int(videoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))

#指定写视频的格式, I420-avi, MJPG-mp4 ,在 Windows 下无法保存
videoWriter = cv2.VideoWriter('output_convert.mp4', cv2.cv.CV_FOURCC('M', 'J', 'P', 'G'), fps, size)

#读帧
success, frame = videoCapture.read()

while success :
    cv2.imshow('videoCapture', frame) #显示
    cv2.waitKey(1000/int(fps)) #延迟
    videoWriter.write(frame) #写视频帧
    success, frame = videoCapture.read() #获取下一帧
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

使用 `openCV 3.0.0` 进行视频拍摄

```
# coding=utf-8

import numpy as np
import cv2

cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.flip(frame,0)

        # write the flipped frame
        out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
```
