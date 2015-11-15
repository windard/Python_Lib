#coding=utf-8
import Image
pic = Image.open("../images/test.jpg")
#打印图片对象
print pic
#打印图片大小
print pic.size
#打印图片编码格式
print pic.mode
#打印图片保存格式
print pic.format