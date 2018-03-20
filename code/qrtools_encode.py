# coding=utf-8

import qrtools

qr = qrtools.QR('qrtools encoder')
print "type:", qr.data_recognise()

qr.encode('qrtools_encode.png')
