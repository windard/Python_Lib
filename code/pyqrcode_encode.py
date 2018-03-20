# coding=utf-8

from pyqrcode import QRCode

data = QRCode("hello world")

print data.text()
data.png('pyqrcode_encode.png',
    scale=5,
    module_color=(0x66, 0x33, 0x0),
    background=(0xff, 0xff, 0xff, 0x88))
