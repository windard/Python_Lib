#coding=utf-8
	
data = """
5A 02 02 77 20 7D 02 75 3F 20 0C 02 08 20 06 02
7F 09 78 77 20 02 01 78 20 00 02 05 78 20 76 7B
74 7F 7F 78 01 7A 78 20 7C 01 20 0C 02 08 05 20
7D 02 08 05 01 78 0C 41 20 67 7B 7C 06 20 02 01
78 20 0A 74 06 20 79 74 7C 05 7F 0C 20 78 74 06
0C 20 07 02 20 76 05 74 76 7E 41 20 6A 74 06 01
3A 07 20 7C 07 52 20 44 45 4B 20 7E 78 0C 06 20
7C 06 20 74 20 04 08 7C 07 78 20 06 00 74 7F 7F
20 7E 78 0C 06 03 74 76 78 3F 20 06 02 20 7C 07
20 06 7B 02 08 7F 77 01 3A 07 20 7B 74 09 78 20
07 74 7E 78 01 20 0C 02 08 20 07 02 02 20 7F 02
01 7A 20 07 02 20 77 78 76 05 0C 03 07 20 07 7B
7C 06 20 00 78 06 06 74 7A 78 41 20 6A 78 7F 7F
20 77 02 01 78 3F 20 0C 02 08 05 20 06 02 7F 08
07 7C 02 01 20 7C 06 20 7A 75 00 7A 01 7C 7B 05
76 76 76 7A 41 
"""
data1 = data.replace(" ","")
data2 = data1.replace("\n","")
data3 = data2.decode("hex")
def chang(j,i):
	if ord(j)+i >=128:
		return chr(ord(j)+i-128)
	else:
		return chr(ord(j)+i)
	
for i in range(128):
	l = ""
	for j in data3:
		j = chang(j,i)
		l = l+j
	# if "ZJPC" in l:
	# 	print l
	print l