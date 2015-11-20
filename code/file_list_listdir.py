import os

def showall(path,leavel=0,filenum=0,dirnum=0,show=True):
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
			# print tab_stop + newpath
			num,numdir = showall(newpath,leavel+1,newnum,oldnum,show)
			newnum = num
			oldnum = numdir
		else:
			newnum = newnum + 1
			tab_stop = ""
			if show:
				for tab in range(leavel):
					tab_stop = tab_stop + "    "
			print tab_stop + newpath

	return newnum,oldnum

if __name__ == '__main__':
	filenum,dirnum = showall(r'C:\Users\dell\Desktop\2048',show=False)
	print "File Number : " + str(filenum)
	print "Dir  Number : " + str(dirnum)
