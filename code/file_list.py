import os
# # print os.getcwd()
# def func():
# 	pass
# # os.sep
# # os.getcwd()
# # print os.listdir()
# # print os.walk(os.getcwd())
dirlist = r"C:\Users\dell\Desktop\2048"
filenum = 0
dirnum  = 0
for i,j,k in os.walk(dirlist):
	print i
for i,j,k in os.walk(dirlist):
	for item in k:
		print item
	filenum = filenum + 1
	for index in range(len(k)):
		dirnum = dirnum + 1

print filenum
print dirnum




# import os

# def showall(path,leavel=0,filenum=0,dirnum=0,show=True):
# 	newnum = filenum
# 	oldnum = dirnum
# 	currentpath = path;
# 	dirandfile = os.listdir(path)
# 	for item in dirandfile:
# 		newpath = os.path.join(currentpath,item)
# 		if os.path.isdir(newpath):
# 			oldnum = oldnum + 1			
# 			tab_stop = ""
# 			if show:
# 				for tab in range(leavel):
# 					tab_stop = tab_stop + "    "
# 			# print tab_stop + newpath
# 			num,numdir = showall(newpath,leavel+1,newnum,oldnum,show)
# 			newnum = num
# 			oldnum = numdir
# 		else:
# 			newnum = newnum + 1
# 			tab_stop = ""
# 			if show:
# 				for tab in range(leavel):
# 					tab_stop = tab_stop + "    "
# 			print tab_stop + newpath

# 	return newnum,oldnum

# if __name__ == '__main__':
# 	filenum,dirnum = showall(r'C:\Users\dell\Desktop\other thing',show=False)
# 	print "File Number : " + str(filenum)
# 	print "Dir  Number : " + str(dirnum)