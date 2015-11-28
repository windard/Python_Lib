#coding=utf-8

import os
import argparse

def showall(path,leavel=0,filenum=0,dirnum=0,show=True,showtype=True,save=False):
	newnum = filenum
	oldnum = dirnum
	currentpath = path;
	dirandfile = os.listdir(path)
	for item in dirandfile:
		newpath = os.path.join(currentpath,item)
		if os.path.isdir(newpath):
			oldnum = oldnum + 1			
			tab_stop = ""
			if show:
				for tab in range(leavel):
					tab_stop = tab_stop + "    "
			if not showtype:
				if not save:
					print tab_stop + newpath
				else:
					savefile = open(save,"a")
					savefile.write(tab_stop+newpath+"\n")
					savefile.close()
			num,numdir = showall(newpath,leavel+1,newnum,oldnum,show,showtype,save)
			newnum = num
			oldnum = numdir
		else:
			newnum = newnum + 1
			tab_stop = ""
			if show:
				for tab in range(leavel):
					tab_stop = tab_stop + "    "
			if showtype:
				if not save:
					print tab_stop + newpath
				else:
					savefile = open(save,"a")
					savefile.write(tab_stop+newpath+"\n")
					savefile.close()
	return newnum,oldnum

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Show All Your File")
	parser.add_argument("-o","--on",help="show the inden",action="store_true")
	parser.add_argument("-d","--dir",help="show dirs",action="store_true")
	parser.add_argument("begin",help="begin your files",action="store",default=r"./")
	parser.add_argument("--save",help="print or save files",action="store",default=False)
	args = parser.parse_args()
	showtype = True
	if args.dir:
		showtype=False
	if args.on:
		show = True
	else:
		show = False
	begin = args.begin
	save  = args.save
	filenum,dirnum = showall(begin,show=show,showtype=showtype,save=save)
	if showtype:
		print "File Number : " + str(filenum)
	else:
		print "Dir  Number : " + str(dirnum)	
