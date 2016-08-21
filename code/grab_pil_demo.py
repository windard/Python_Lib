#coding=utf-8

from PIL import ImageGrab

img = ImageGrab.grab()

# img = ImageGrab.grab((10,10,510,510))

img.save('grab_pil_demo.png','PNG')