#coding=utf-8
import Image
#生成一张新的图片
pic1 = Image.new("RGB",(600,600),(255,147,89))
# pic1 = Image.open("../images/test1.png")
#打开一张图片
pic2 = Image.open("../images/test2.jpg")
#先把第二张图片的编码格式转化为与第一张相同
pic2.convert(pic1.mode)
#把两张图片结合到一起
pic3 = Image.blend(pic1,pic2,0.3)
pic3.show()
pic3.save("../images/test4.jpg")