import os 
import requests

path = 'C:\\Users\\dell\\Desktop\\python\\Web_Spider'
url  = 'http://localhost/upload/1/upload.php'
dirAndFile = os.listdir(path)
filenum = 0
for item in dirAndFile:
	itemdir = os.path.join(path,item)
	if os.path.isdir(itemdir):
		print "This is a dir : " + itemdir
	else :
		files = {'file': open(itemdir, 'rb'),}
		data  = {'submit':'true'}   
		page = requests.post(url, data=data,files=files)
		code = page.status_code
		if 	code == 200:
			filenum = filenum + 1
			print  "No " + str(filenum) + " Upload Successful !"
		else :
			print "Upload Failed!"


