#coding=utf-8

import rsa
import sys
import base64
import hashlib
import binascii
import argparse
from Crypto.Cipher import AES
from Crypto.Cipher import DES
from Crypto.Cipher import DES3

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
	elif dotype.lower().startswith("hex"):
		return binascii.b2a_hex(data)
	else:
		return "Sorry,Your Input Is Wrong,Please Try Again"

def decode(dotype,data):
	if dotype.lower().startswith("base64"):
		return base64.b64decode(data)
	elif dotype.lower().startswith("base32"):
		return base64.b32decode(data)
	elif dotype.lower().startswith("base16"):
		return base64.b16decode(data)
	elif dotype.lower().startswith("hex"):
		return binascii.a2b_hex(data)
	else:
		return "Sorry,Your Input Is Wrong,Please Try Again"

def encode_rsa(data,length):
	(pubkey,privkey) = rsa.newkeys(length)
	crypto = rsa.encrypt(data,pubkey)
	return str(pubkey.save_pkcs1())+"\n"+str(privkey.save_pkcs1())+"\n"+crypto.encode("base64")

def encode_des(data,key,IV):
	if len(data)%8 !=0:
		return "Sorry,Your Input Is Wrong,Data Must Be A Multiple Of 8"	
	d = DES.new(key,DES.MODE_CBC,IV)
	cipher = d.encrypt(data)
	results = base64.b64encode(cipher)
	return results

def encode_des3(data,key,IV):
	if len(data)%8 !=0:
		return "Sorry,Your Input Is Wrong,Data Must Be A Multiple Of 8"
	d = DES3.new(key,DES3.MODE_CBC,IV)
	cipher = d.encrypt(data)
	results = base64.b64encode(cipher)
	return results

def encode_aes(data,key,IV):
	if len(data)%16 !=0:
		return "Sorry,Your Input Is Wrong,Data Must Be A Multiple Of 16"	
	mode = AES.MODE_CBC
	encryptor = AES.new(key, mode,IV)
	ciphertext = encryptor.encrypt(data)
	results = base64.b64encode(ciphertext)
	return results

def decode_rsa(data,privkey):
	return rsa.decrypt(data,privkey)

def decode_des(data,key,IV):
	m = DES.new(key,DES.MODE_CBC,IV)
	cipher = base64.b64decode(data)
	results = m.decrypt(cipher)
	return results

def decode_des3(data,key,IV):
	m = DES3.new(key,DES3.MODE_CBC,IV)
	cipher = base64.b64decode(data)
	results = m.decrypt(cipher)
	return results

def decode_aes(data,key,IV):
	mode = AES.MODE_CBC
	decryptor = AES.new(key, mode,IV)
	ciphertext = base64.b64decode(data)
	results = decryptor.decrypt(ciphertext)
	return results

if __name__ == '__main__':  
	parser = argparse.ArgumentParser(description="Select your decode&encode type")
	parser.add_argument("-d","--decode",help="decode data",action="store_true")
	parser.add_argument("-e","--encode",help="encode data",action="store_true")
	parser.add_argument("-f","--file",help="decode file",action="store_true")
	parser.add_argument("--type",help="decode or encode type",action="store",default="md5",dest="dotype")
	parser.add_argument("--length",help="RSA encode length",action="store",default=1024,type=int,dest="length")
	parser.add_argument("--key",help="DES or DES3 or AES encode or decode key or RSA privkey",action="store",default="01234567",dest="key")
	parser.add_argument("--IV",help="DES or DES3 or AES encode or decode IV",action="store",default="abcdefgl",dest="IV")
	parser.add_argument("--data",help="decode or encode data",action="store",dest="data")
	parser.add_argument("--filename",help="select your file",action="store",dest="filename")
	parser.add_argument("--save",help="input stdio or text",action="store",default=False,dest="save")
	args = parser.parse_args()
	data = args.data
	dotype = args.dotype
	length = args.length
	key = args.key
	IV = args.IV
	filename = args.filename
	save = args.save
	if args.encode:
		if dotype.lower().startswith("rsa"):
			results = encode_rsa(data,length)
		elif dotype.lower().startswith("des3"):
			results = encode_des3(data,key+IV,IV)
		elif dotype.lower().startswith("des"):
			results = encode_des(data,key,IV)			
		elif dotype.lower().startswith("aes"):
			results = encode_aes(data,key+IV,IV+key)
		else:
			results = encode(dotype,data)
	elif args.decode:
		if dotype.lower().startswith("rsa"):
			results = decode_rsa(data,key)
		elif dotype.lower().startswith("des3"):
			results = decode_des3(data,key+IV,IV)			
		elif dotype.lower().startswith("des"):
			results = decode_des(data,key,IV)
		elif dotype.lower().startswith("aes"):
			results = decode_aes(data,key+IV,IV+key)
		else:
			results = decode(dotype,data)
	elif args.file:
		results = decodeFile(dotype,filename)

	if not save:
		print results
	else:
		resultfile = open(save,"a")
		resultfile.write(results+"\n")
		resultfile.close()

