#coding=utf-8

import os
import argparse

filenum = 0
dirnum  = 0

def listfile(rootlist,showtype=True,save=False):
	global filenum
	global dirnum
	for i,j,k in os.walk(rootlist):
		if not showtype:
			if not save:
				print i
			else:
				savefile = open(save,"a")
				savefile.write(i+"\n")
				savefile.close()
		dirnum = dirnum + 1
		for item in k:
			if showtype:
				if not save:
					print item
				else:
					savefile = open(save,"a")
					savefile.write(item+"\n")
					savefile.close()
			filenum = filenum +1

if __name__ == '__main__':  
	parser = argparse.ArgumentParser(description="Show All Your File")
	parser.add_argument("-d","--dir",help="show dirs",action="store_true")
	parser.add_argument("begin",help="begin your files",action="store",default=r"./")
	parser.add_argument("--save",help="print or save files",action="store",default=False)
	args = parser.parse_args()
	showtype = True
	if args.dir:
		showtype=False
	else:
		show = False
	begin = args.begin
	save  = args.save
	listfile(begin,showtype=showtype,save=save)
	if showtype:
		print "File Number : " + str(filenum)
	else:
		print "Dir  Number : " + str(dirnum)		
