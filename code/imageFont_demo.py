#coding=utf-8
import Image,ImageFont,ImageDraw
pic = Image.open("../images/test2.jpg")
font = ImageFont.truetype("arial.ttf",10)
pic = ImageDraw.Draw(pic)
pic.text((10,10),"Hello world",font=font)
pic.show()
