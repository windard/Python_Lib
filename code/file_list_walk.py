import os

filenum = 0
dirnum  = 0


def listfile(rootlist):
	# for i,j,k in os.walk(rootlist):
	# 	print i
	# for i,j,k in os.walk(rootlist):
	# 	for item in k:
	# 		print item
	# 	filenum = filenum + 1
	# 	for index in range(len(k)):
	# 		dirnum = dirnum + 1
	global filenum
	global dirnum
	for i,j,k in os.walk(rootlist):
		print i
		dirnum = dirnum + 1
		for item in k:
			print item
			filenum = filenum +1

if __name__ == '__main__':  
	rootlist = r"C:\Users\dell\Desktop\2048"
	listfile(rootlist)
	# for i,j,k in os.walk(rootlist):
	# 	print i
	# 	print j
	# 	print k
	print filenum
	print dirnum