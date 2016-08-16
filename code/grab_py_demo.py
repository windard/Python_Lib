#coding=utf-8

import pyscreenshot

def main():
	# 截全屏
	im=pyscreenshot.grab()
	# 查看截屏图片
	# im.show()

	# 保存图片
	pyscreenshot.grab_to_file('grab_py_demo.png')
	
if __name__ == '__main__':
	main()
