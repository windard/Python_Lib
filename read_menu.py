import os 

path = 'C:\\Users\\dell\\Desktop\\python\\Web_Spider'
dirAndFile = os.listdir(path)
filenum = 0
# print dirAndFile
FILE = open('list.txt','w')
# print dirAndFile
for item in dirAndFile:
	# item = item.strip()
	itemdir = os.path.join(path,item)
	if os.path.isdir(itemdir):
		item = item + "\n"
		FILE.write("This is a dir : ---------------------------------" + item)
		filenum = filenum + 1
	else :
		item = item + "\n"
		FILE.write(item)
		filenum = filenum + 1
	# print item
FILE.write("All File is :" + str(filenum))
FILE.close()

# OtherFile = open('list.txt','r')
# print OtherFile