#coding=utf-8
import Image,ImageDraw
pic = Image.open("../images/test2.jpg")
draw = ImageDraw.Draw(pic)
width,height = pic.size

#画两条对角线
draw.line(((0,0),(width-1,height-1)),fill=(136,56,99))
draw.line(((0,height-1),(width-1,0)),fill=(6,156,209))

#画一个圆
draw.arc((0,0,width-1,height-1),0,360,fill=(255,255,0))
pic.show()
pic.save("../images/test5.jpg")