# -*- coding: utf-8 -*-

from PIL import Image, ImageFilter


img = Image.open("card.jpeg")
im = img.filter(ImageFilter.GaussianBlur(25))

im.show()
