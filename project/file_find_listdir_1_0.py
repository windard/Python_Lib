#coding=utf-8

import os
import argparse

findnum = 0

def findFile(path,filename):
	global findnum
	currentpath = path;
	dirandfile = os.listdir(path)
	for item in dirandfile:
		newpath = os.path.join(currentpath,item)
		if os.path.isdir(newpath):
			findFile(newpath,filename)
		else:
			if filename in newpath:
				findnum = findnum+1
				print newpath

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Find Your File")
	parser.add_argument("begin",help="begin your files",action="store",default=r"./")
	parser.add_argument("filename",help="your filename",action="store")
	args = parser.parse_args()
	begin = args.begin
	filename = args.filename
	findFile(begin,filename=filename)
	print "FOUND FILES: " + str(findnum)
