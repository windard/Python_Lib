# coding=utf-8

import numpy as np
import cv2
from matplotlib import pyplot as plt

img=cv2.imread('lena.png',cv2.IMREAD_COLOR)

# 恢复原色
img1 = img[:, :, ::-1]
plt.imshow(img1)
plt.show()

# 上下翻转
img2 = img1[::-1]
plt.imshow(img2)
plt.show()

# 左右翻转
img3 = img1[:, ::-1]
plt.imshow(img3)
plt.show()

# 逆时针旋转
