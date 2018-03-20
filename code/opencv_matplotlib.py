# coding=utf-8

import cv2
from matplotlib import pyplot as plt

img = cv2.imread("lena.png", cv2.IMREAD_COLOR)
plt.imshow(img)
plt.show()
