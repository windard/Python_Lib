# # coding=utf-8

# import cv2.cv as cv

# capture = cv.CaptureFromCAM(0)
# temp = cv.QueryFrame(capture)
# writer = cv.CreateVideoWriter("output.avi", cv.CV_FOURCC("M","J","P","G"), 25, cv.GetSize(temp), 1)

# count = 0
# while count < 500:
#     image = cv.QueryFrame(capture)
#     cv.WriteFrame(writer, image)
#     cv.ShowImage('Image_Window',image)
#     cv.WaitKey(1)
#     count += 1

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