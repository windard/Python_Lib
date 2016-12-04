# coding=utf-8

import time
import cv2
import cv2.cv as cv
import numpy as np  

win_name = "Webcam"
capture = cv.CaptureFromCAM(0)

cv.NamedWindow(win_name, cv.CV_WINDOW_AUTOSIZE)

# 定义一个无限循环
while 1:

    # 每次从视频数据流框架中抓取一帧图片
    image = cv.QueryFrame(capture)

    # 将图片显示在特定窗口上
    cv.ShowImage(win_name, image)

    # 当安县Esc键时退出循环
    c = cv.WaitKey(1)
    if c == 27:
        break
    elif c == 13:
        emptyImage = np.zeros(image.shape, np.uint8) 
        # emptyImage2 = image.copy()
        # emptyImage3 = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        cv2.imwrite("Capture"+time.strftime('%Y-%m-%d %H:%M:%S')+".jpg", emptyImage)

# 退出循环后销毁显示窗口
cv.DestroyWindow(win_name)