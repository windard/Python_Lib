# -*- coding: utf-8 -*-

from PIL import Image
from pyzbar.pyzbar import decode


d = decode(Image.open("qrcode_demo.png"))
print d
print d[0].data
