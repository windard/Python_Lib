# coding=utf-8

import sys
import pyqrcode

data = pyqrcode.create(u"你好，世界", encoding="utf-8")
data.svg(sys.stdout, scale=1)
data.svg("pyqrcode_demo.svg", scale=4)
data.png("pyqrcode_demo.png", scale=4)
data.show()

number = pyqrcode.create(123456789012345)
number.png('big-number.png')
print number.png_as_base64_str()
print number.terminal()
