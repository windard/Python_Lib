# # coding=utf-8

# import numpy as np
# import cv2

# cap = cv2.VideoCapture('output.avi')

# while(cap.isOpened()):
#     ret, frame = cap.read()

#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     cv2.imshow('frame',gray)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

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