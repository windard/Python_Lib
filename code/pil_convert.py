# coding=utf-8

from PIL import Image, ImageFile

from exceptions import IOError

img = Image.open("code.jpg")
des = "code_progress.jpg"

try:
	img.save(des, "JPEG", quality=80, optimize=True, progressive=True)
except IOError:
	ImageFile.MAXBLOCK = img.size[0] * img.size[1]
	img.save(des, "JPEG", quality=80, optimize=True, progressive=True)