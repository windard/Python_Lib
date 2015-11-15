import Image
pic = Image.open("../images/test.jpg")
for i in  range(len(pic.histogram())):
	if i%30==0 and i!=0:
		print ""	
	print pic.histogram()[i],
	