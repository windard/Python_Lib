#coding=utf-8

import os
import argparse

findnum = 0

def findFile(rootlist,filename):
	global findnum
	for i,j,k in os.walk(rootlist):
		for item in k:
			if filename in item:
				findnum = findnum + 1
				print item
				
if __name__ == '__main__':  
	parser = argparse.ArgumentParser(description="Show All Your File")
	parser.add_argument("begin",help="begin your files",action="store",default=r"./")
	parser.add_argument("filename",help="your filename",action="store")
	args = parser.parse_args()
	begin = args.begin
	filename = args.filename
	findFile(begin,filename)
	print "FOUND FILES: " + str(findnum)

