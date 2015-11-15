#coding=utf-8
import Image,ImageFilter
pic = Image.open("../images/test2.jpg")
pic1 = pic.filter(ImageFilter.BLUR)
pic1.show()
pic1.save("../images/test9.jpg")