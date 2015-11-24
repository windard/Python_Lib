#coding=utf-8
import rsa

#生成1024位的公钥和私钥
(pubkey,privkey) = rsa.newkeys(1024)

#将密钥保存成pem格式，也可以直接使用

#公钥
pub = pubkey.save_pkcs1()
pubfile = open("pubfile.pem","w")
pubfile.write(pub)
pubfile.close()

#私钥
priv = privkey.save_pkcs1()
privfile = open("privfile.pem","w")
privfile.write(priv)
privfile.close()

#导出pem格式的公钥和私钥
with open("pubfile.pem") as publickfile:
	p = publickfile.read()
	pubkey = rsa.PublicKey.load_pkcs1(p)

with open("privfile.pem") as privlickfile:
	p = privlickfile.read()
	privkey = rsa.PrivateKey.load_pkcs1(p)


message = "hello"

#加密信息
crypto = rsa.encrypt(message,pubkey)
#解密信息
message = rsa.decrypt(crypto,privkey)

#用私钥签名认证，用公钥验证签名
signature = rsa.sign(message,privkey,'SHA-1')
rsa.verify("hello",signature,pubkey)
