#coding=utf-8
import hashlib
import argparse
import base64
import sys

BLOCK = 2**20

def decodeFile(dotype,filename):
	filename = open(filename,"rb")
	if dotype.lower().startswith("md5"):
		decode = hashlib.md5()
	elif dotype.lower().startswith("sha1"):
		decode = hashlib.sha1()
	else:
		return "Sorry,Your Input Is Wrong,Please Try Again"
	while True:
		data = filename.read(BLOCK)
		if not data:
			break
		decode.update(data)
	return decode.hexdigest()

def encode(dotype,data):
	if dotype.lower().startswith("base64"):
		return base64.b64encode(data)
	elif dotype.lower().startswith("base32"):
		return base64.b32encode(data)
	elif dotype.lower().startswith("base16"):
		return base64.b16encode(data)
	elif dotype.lower().startswith("md5"):
		encode = hashlib.md5()
		encode.update(data)
		return encode.hexdigest()
	elif dotype.lower().startswith("sha1"):
		encode = hashlib.sha1()
		encode.update(data)
		return encode.hexdigest()
	else:
		return "Sorry,Your Input Is Wrong,Please Try Again"

def decode(dotype,data):
	if dotype.lower().startswith("base64"):
		return base64.b64decode(data)
	elif dotype.lower().startswith("base32"):
		return base64.b32decode(data)
	elif dotype.lower().startswith("base16"):
		return base64.b16decode(data)
	elif dotype.lower().startswith("ord"):
		try:
			return ord(data)
		except:
			return "Sorry,Your Input Is Wrong,Please Try Again"
	else:
		return "Sorry,Your Input Is Wrong,Please Try Again"


if __name__ == '__main__':  
	parser = argparse.ArgumentParser(description="Select your decode&encode type")
	parser.add_argument("-d","--decode",help="decode data",action="store_true")
	parser.add_argument("-e","--encode",help="encode data",action="store_true")
	parser.add_argument("-f","--file",help="decode file",action="store_true")
	parser.add_argument("--type",help="decode or encode type",action="store",default="md5",dest="dotype")
	parser.add_argument("--data",help="decode or encode data",action="store",dest="data")
	parser.add_argument("--filename",help="select your file",action="store",dest="filename")
	parser.add_argument("--save",help="input stdio or text",action="store",default=False,dest="save")
	args = parser.parse_args()
	data = args.data
	dotype = args.dotype
	filename = args.filename
	save = args.save
	if args.encode:
		results = encode(dotype,data)
	elif args.decode:
		results = decode(dotype,data)
	elif args.file:
		results = decodeFile(dotype,filename)
	if not save:
		print results
	else:
		resultfile = open(save,"a")
		resultfile.write(results+"\n")
		resultfile.close()

