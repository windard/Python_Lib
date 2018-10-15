# -*- coding: utf-8 -*-
# coding=utf-8

from PIL import Image

im = Image.open('card.jpeg')
r, g, b = im.split()
h,w = im.size
print h,w

# 创建一个新的 r 通道分量, 注意 mode 值为 'L'
# 255 是白
# 0 是黑
n = Image.new('L', (h, w), color=0)

for i in range(h):
    for j in range(w):
        pixel = im.getpixel((i, j))
        if all(map(lambda x:x>210, pixel)):
            im.putpixel((i, j), (0, 0, 255))
# im = Image.merge('RGB', (n, n, b))
im.show()

