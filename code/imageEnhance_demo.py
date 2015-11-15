#coding=utf-8
import Image,ImageEnhance
pic = Image.open("../images/test2.jpg")

#亮度增强
brightness = ImageEnhance.Brightness(pic)
bright_pic = brightness.enhance(2.0)
bright_pic.show()
bright_pic.save("../images/test6.jpg")

#图像尖锐化
sharpness = ImageEnhance.Sharpness(pic)
sharp_pic = sharpness.enhance(5.0)
sharp_pic.show()
sharp_pic.save("../images/test7.jpg")

#对比度增强
contrast = ImageEnhance.Contrast(pic)
contrast_pic = contrast.enhance(3.0)
contrast_pic.show()
contrast_pic.save("../images/test8.jpg")