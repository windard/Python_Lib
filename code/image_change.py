#coding=utf-8
import Image
pic = Image.open("../images/test.jpg")

#改变图像大小
pic1 = pic.resize((600,600))
# pic1.show()
print pic1.size
#保存图片,也可以同时改变图片格式
pic1.save("../images/test1.png")
print pic1.mode
print pic1.format

#剪裁图片
pic2 = pic.crop((0,200,600,800))
# pic2.show()
print pic2.size
#保存图片
pic1.save("../images/test2.jpg")
print pic2.mode
print pic2.format

#旋转图片
pic3 = pic2.rotate(45)
pic3.show()
#保存图片
pic3.save("../images/test3.jpg")


