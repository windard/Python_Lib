# coding=utf-8

import qrcode

qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
qr.add_data('this is a new qrcode')

qr.print_ascii()
qr.print_tty()


img = qr.make_image()
img.show()
img.save('qrcode_high.png')
