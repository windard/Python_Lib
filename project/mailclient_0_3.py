import poplib
import email
import sys
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

#Reseive Information
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

#Send Content
def sendMessage():
	subject = raw_input("Please Input Your Email Subject\n")
	content = raw_input("Please Input Your Email Content:\n")
	return (subject,content)

#show mail attachment
def showAttachment(msg):
	maintype=msg.get_content_maintype()
	if maintype == 'multipart':
		for part in msg.get_payload():
			showAttachment(part)
	elif maintype == 'text':
		if  not msg["Content-Disposition"]:
			pass
		else:
			print "This mail has an Attachment"
			filename = msg["Content-Disposition"].split("\"")[-2]
			print "File Name: "+filename
			print ""

#show mail subject
def showSubject(msg):
	try:
		print msg["Subject"]
		print ""
	except:
		print ""	
		pass
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
		messageSubject,messageContent = sendMessage()
		message = MIMEText(messageContent)
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
		for index in range(1,len(mails)+1):
			resp, lines, octets = popObj.retr(index)
			msg_content = '\r\n'.join(lines)
			msg = Parser().parsestr(msg_content)
			print "This Is No.%s Mail Subject :"%index
			showSubject(msg)
			showAttachment(msg)



