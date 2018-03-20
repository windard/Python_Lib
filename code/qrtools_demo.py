# coding=utf-8

import qrtools

qr = qrtools.QR(filename='qrcode_demo.png')
print "type:", qr.data_recognise()

res = qr.decode()
if res:
    print "data:", qr.data
else:
    print("Error")
