#coding=utf-8

import pyscreenshot

def main():
	# 截部分屏幕
	im=pyscreenshot.grab(bbox=(10,10,510,510)) 
	# 查看截屏图片
	# im.show()

	# 保存图片
	pyscreenshot.grab_to_file('grab_py_part.png')

if __name__ == '__main__':
	main()