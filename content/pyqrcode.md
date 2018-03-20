## pyqrcode

python 实现的二维码生成库, 并不能解析二维码

可以使用 `qrcode -o filename input` 来生成二维码，生成 png 图片，不能直接显示在终端

### 生成二维码

```
# coding=utf-8

import sys
import pyqrcode

data = pyqrcode.create(u"你好，世界", encoding="utf-8")
data.svg(sys.stdout, scale=1)
data.svg("pyqrcode_demo.svg", scale=4)
data.show()

number = pyqrcode.create(123456789012345)
number.png('big-number.png')
print number.png_as_base64_str()
print number.terminal()

```

也可以使用对象的方式

```
# coding=utf-8

from pyqrcode import QRCode

data = QRCode("hello world")

print data.text()
data.png('pyqrcode_encode.png',
    scale=5,
    module_color=(0x66, 0x33, 0x0),
    background=(0xff, 0xff, 0xff, 0x88))

```
