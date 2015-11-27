import poplib
import email
import sys
import os
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print "Welcome To MailClient"

#Chose sendOrReceive
def sendOrReceive():
	workType = raw_input("Please Chose Work Type:[send/receive]\n")
	if workType.lower().startswith("send"):
		print "You Chose Send"
		return 1
	elif workType.lower().startswith("receive"):
		print "You Chose Receive" 
		return 2
	else:
		print "Your Input Is Wrong,Please Input Aganin"	
		workType = sendOrReceive()
		return workType

#Send Information
def sendInfo():
	while True:
		email_host = raw_input("Please Input Your Email_host:\n")
		if email_host.lower().startswith("qq"):
			email_host = "smtp.qq.com"
		elif email_host.lower().startswith("163"):
			email_host = "smtp.163.com"
		else:
			pass
		if connSendServer(email_host):
			break	
	while True:
		from_email = raw_input("Please Input From_email:\n")
		password   = raw_input("Please Input Your Password:\n")
		smtpObj = smtplib.SMTP_SSL(email_host)		
		if sendLogin(smtpObj,from_email,password):
			break	
	to_email   = raw_input("Please Input To_email:\n")
	return (email_host,from_email,to_email,password)

#Receive Information
def receiveInfo():
	while True:
		email_host = raw_input("Please Input Your Email_host:\n")
		if email_host.lower().startswith("qq"):
			email_host = "pop.qq.com"
		elif email_host.lower().startswith("163"):
			email_host = "pop.163.com"
		else:
			pass
		if connReceServer(email_host):
			break
	while True:
		email      = raw_input("Please Input Your Email:\n")
		password   = raw_input("Please Input Your Password:\n")
		popObj = poplib.POP3_SSL(email_host)
		if receLogin(popObj,email,password):
			break
	return (email_host,email,password)

#Connect Receive Server
def connReceServer(email_host):
	try:
		try:
			popObj = poplib.POP3_SSL(email_host)
		except:
			popObj = poplib.POP3(email_host)
		print popObj.getwelcome()+"\n"
		return 1
	except:
		print "There is something wrong with your email_host,Please Try Aganin"	
		return 0

#Connect Send Server
def connSendServer(email_host):
	try:
		smtpObj = smtplib.SMTP_SSL(email_host)
		return 1
	except:
		print "There is something wrong with your email_host,Please Try Aganin"	
		return 0

#send login
def sendLogin(smtpObj,from_email,password):
	try:
		smtpObj.login(from_email,password)
		return 1
	except:
		print "Your Username Or Password Is Wrong,Please Try Aganin"
		return 0

#receive login
def receLogin(popObj,email,password):
	try:
		popObj.user(email)
		popObj.pass_(password)
		return 1
	except:
		print "Your Username Or Password Is Wrong,Please Try Aganin"
		return 0	

#chose send type
def sendType():
	sendtype = raw_input("Please Input Your Send Type:[plain/html/multi]\n")
	if sendtype.lower().startswith("plain"):
		return 1
	elif sendtype.lower().startswith("html"):
		return 2
	elif sendtype.lower().startswith("multi"):
		return 3
	else:
		print "Your Chose Is Wrong,Please Try Aganin"
		return 0

#Send Content
def sendMessage():
	subject = raw_input("Please Input Your Email Subject\n")
	content = raw_input("Please Input Your Email Content:\n")
	return (subject,content)

#show mail attachment
def showAttachment(msg):
	maintype=msg.get_content_type()
	if maintype.lower().startswith('multipart'):
		for part in msg.get_payload():
			showAttachment(part)
	elif maintype.lower().endswith("base64"):
		if  not msg["Content-Disposition"]:
			pass
		else:
			print "-"*50
			print "This mail has an Attachment"
			filename = msg["Content-Disposition"].split("\"")[-2]
			print "File Name: "+filename
			print ""
	else:
		pass

#download attachment
def downloadAttachment(msg):
	maintype=msg.get_content_type()
	if maintype.lower().startswith('multipart'):
		for part in msg.get_payload():
			downloadAttachment(part)
	elif maintype.lower().endswith("base64"):
		if  not msg["Content-Disposition"]:
			pass
		else:
			download = raw_input("Do You Want To Download The Attachment?[yes|no]\n")
			if download.lower().startswith("no"):
				print "OK,Do Not Download"
				pass
			else:
				filename = msg["Content-Disposition"].split("\"")[-2]
				downloadfile = open(filename,"wb")
				downloadfile.write(msg.get_payload(decode=True))
				downloadfile.close()
				print "Download Successful"

#show mail subject
def showSubject(msg):
	try:
		subdecode = decode_header(msg["Subject"])[0][1]
		if not subdecode==None:
			print  decode_header(msg["Subject"])[0][0].decode(decode_header(msg["Subject"])[0][1]).encode("utf-8")
		else:
			print unicode(decode_header(msg["Subject"])[0][0],"utf-8")	
		print ""
	except:
		print ""	
		pass
		
#show mail from and to		
def showMoreInfo(msg):
	try:
		from_email_decode = decode_header(msg["from"])[0][1]
		if not from_email_decode==None:
			print  "From: " + decode_header(msg["from"])[0][0].decode(decode_header(msg["from"])[0][1]).encode("utf-8")
		else:
			print "From: " + unicode(decode_header(msg["from"])[0][0],"utf-8")	
		to_email_decode = decode_header(msg["to"])[0][1]
		if not to_email_decode==None:
			print  "To  : " + decode_header(msg["to"])[0][0].decode(decode_header(msg["to"])[0][1]).encode("utf-8")
		else:
			print "To  : " + unicode(decode_header(msg["to"])[0][0],"utf-8")	
	except:
		print ""
		pass

#show mail content
def showContent(msg):
	contentType = msg.get_content_type()
	if contentType.lower().startswith("multipart"):
		for i in msg.get_payload():
			showContent(i)
	elif contentType.lower().endswith("base64"):
		pass
	else:
		print msg.get_payload(decode=True)		

#delete single mail
def deleteMail(popObj):
	try:
		deletenum = input("Please Input The Number Mail You Want To Delete: \n")
	except:
		print "Your Input Is Wrong"
		return
	index = int(deletenum)	
	try:
		msg.dele(index)
		print "Delete Number %d Mail Successful"%index
	except:
		print "Delete Mail Failed"

#read single mail
def readMail(popObj):
	try:
		index = input("Please Input The Number Your Want To Read :\n")
	except:
		print "Your Input Is Wrong"
		return
	resp, mails, octets = popObj.list()
	if index > len(mails):
		print "Your Input Is Wrong"
		return 
	print "\n\n\nThe Number %d Mail is: \n"%index
	resp, lines, octets = popObj.retr(index)
	msg_content = '\r\n'.join(lines)
	msg = Parser().parsestr(msg_content)
	showMoreInfo(msg)
	print "Subject :"
	showSubject(msg)
	print "Content :"
	showContent(msg)
	showAttachment(msg)
	downloadAttachment(msg)

#show more subject
def showMoreSubject(popObj):
	try:
		beginnum = int(input("Please Input The Number Begin:\n"))
		endnum   = int(input("Please Input The Number End  :\n"))
	except:
		print "Your Input Is Wrong\n"
		return
	resp, mails, octets = popObj.list()
	if endnum > len(mails)+1:
		endnum = len(mails)+1
	for index in range(beginnum,endnum):
	 	resp, lines, octets = popObj.retr(index)
		msg_content = '\r\n'.join(lines)
		msg = Parser().parsestr(msg_content)
		print "This Is No.%s Mail Subject :"%index
		showSubject(msg)
		showAttachment(msg)


#quit
def Quit():
	print "Thanks For Your Using ."
	print "You Can Report Bugs to 1106911190@qq.com"
	print "PRESS ENTER TO QUIT"
	raw_input()
	sys.exit()

if __name__ == '__main__':  
	workType = sendOrReceive()
	if workType == 1:
		email_host,from_email,to_email,password = sendInfo()
		smtpObj = smtplib.SMTP_SSL(email_host)
		while True:
			sendtype = sendType()
			if sendtype:
				break
		messageSubject,messageContent = sendMessage()
		if not sendtype==3:
			if sendtype==1:
				message = MIMEText(messageContent,_subtype='plain',_charset='utf-8')
			else:
				message = MIMEText(messageContent,_subtype='html',_charset='utf-8')
		else:
			multiName = raw_input("Please Input Your Attachment Name:\n")
			message = MIMEMultipart()
			attr = MIMEText(open(multiName,"rb").read(),"base64","utf-8")
			attr["Content-Type"] = 'application/octet-stream'
			attr["Content-Disposition"] = 'attachment; filename="%s"'%(multiName)
			message.attach(attr)
			content = MIMEText(messageContent,"plain","utf-8")
			message.attach(content)


		message["Subject"] = messageSubject
		message["From"] = from_email
		message["To"] = to_email
		smtpObj.login(from_email,password)
		try:
			smtpObj.sendmail(from_email,to_email,message.as_string())
			print "Sending Successful"
		except:
			print "Sending Failes"
		smtpObj.close()
		Quit()	
		
	elif workType == 2:
		email_host,email,password = receiveInfo()
		popObj = poplib.POP3_SSL(email_host)
		popObj.user(email)
		popObj.pass_(password)
		status = popObj.stat()
		print "MailBox has %d message for a total of %s bytes"%(status[0],status[1])
		resp, mails, octets = popObj.list()
		for index in range(len(mails)-10,len(mails)+1):
		 	resp, lines, octets = popObj.retr(index)
			msg_content = '\r\n'.join(lines)
			msg = Parser().parsestr(msg_content)
			print "This Is No.%s Mail Subject :"%index
			showSubject(msg)
			showAttachment(msg)

		print "\n\n\nThe Lastest Mail is: \n"
		index = len(mails)
		resp, lines, octets = popObj.retr(index)
		msg_content = '\r\n'.join(lines)
		msg = Parser().parsestr(msg_content)
		showMoreInfo(msg)
		print "Subject :"
		showSubject(msg)
		print "Content :"
		showContent(msg)
		showAttachment(msg)
		downloadAttachment(msg)

		while True:
			continueType = raw_input("Please Input The Next You Want To Do:[read|delete|quit|more]\n")
			if continueType.lower().startswith("read"):
				readMail(popObj)
			elif continueType.lower().startswith("delete"):
				deleteMail(popObj)
			elif continueType.lower().startswith("more"):
				showMoreSubject(popObj)
			else:
				break

		popObj.quit()	
		Quit()
