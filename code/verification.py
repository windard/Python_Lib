# coding=utf-8

import gvcode

img, code = gvcode.generate((240, 60))

print code

img.show()
img.save('verification.jpg')
