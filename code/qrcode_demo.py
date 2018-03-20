# coding=utf-8

import qrcode

img = qrcode.make("hello world")
img.save("qrcode_demo.png")
