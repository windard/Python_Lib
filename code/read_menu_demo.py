#-*-encoding:utf-8-*-
import os,sys

dir = 'C:\\Users\\dell\\Desktop\\python\\Web_Spider'
myfile = open('list.txt','w')
# def listdir(dir,file):
myfile.write(dir +'\n')
fielnum =0
list = os.listdir(dir)#列出目录下的所有文件和目录
for line in list:
	filepath = os.path.join(dir,line)
	if os.path.isdir(filepath):#如果filepath是目录，则再列出该目录下的所有文件
		myfile.write(' '+ line +'//'+'\n')
		for li in os.listdir(filepath):
			myfile.write(' '+li +'\n')
			fielnum = fielnum +1
	elif os.path:#如果filepath是文件，直接列出文件名
		myfile.write(' '+line +'\n')
		fielnum = fielnum +1
	myfile.write('all the file num is '+ str(fielnum))
	# dir = raw_input('please input the path:')
	# myfile = open('list.txt','w')
# listdir(dir,myfile)
# myfile.close()