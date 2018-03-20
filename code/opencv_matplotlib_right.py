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