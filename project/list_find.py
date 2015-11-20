#coding=utf-8

import os
import argparse

findnum = 0

def showall(path,filenum=0,dirnum=0,findfile=False):
	global findnum
	newnum = filenum
	oldnum = dirnum
	currentpath = path;
	dirandfile = os.listdir(path)
	for item in dirandfile:
		newpath = os.path.join(currentpath,item)
		if os.path.isdir(newpath):
			oldnum = oldnum + 1		
			if not findfile:	
				print newpath
		else:
			newnum = newnum + 1
			if not findfile:
				print os.path.basename(newpath)
			else:
				if findfile in newpath:
					findnum = findnum+1
					print os.path.basename(newpath)
	return newnum,oldnum

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Show All Your File")
	parser.add_argument("--list",help="begin your files",action="store",default=r"./")
	parser.add_argument("--file",help="your find files",action="store",default=False)
	args = parser.parse_args()
	listdir = args.list
	findfile = args.file
	filenum,dirnum = showall(listdir,findfile=findfile)
	if not findfile:
		print "File Number : " + str(filenum)
		print "Dir  Number : " + str(dirnum)	
	else:
		print "FOUND　FILES : " + str(findnum)