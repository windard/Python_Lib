## qrtools

qrcode 二维码解析和生成库

看起来小巧易用，实际解析是调用 zbar 库，生成是调用 qrencode 命令。

## 二维码解析

```
# coding=utf-8

import qrtools

qr = qrtools.QR(filename='qrcode_demo.png')
print "type:", qr.data_recognise()

res = qr.decode()
if res:
    print "data:", qr.data
else:
    print("Error")

```

## 二维码生成

```
# coding=utf-8

import qrtools

qr = qrtools.QR('qrtools encoder')
print "type:", qr.data_recognise()

qr.encode('qrtools_encode.png')

```