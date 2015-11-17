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
		if connSendServer(email_host):
			break	
	while True:
		from_email = raw_input("Please Input From_email:\n")
		password   = raw_input("Please Input Your Password:\n")
		smtpObj = smtplib.SMTP(email_host)		
		if sendLogin(smtpObj,from_email,password):
			break	
	to_email   = raw_input("Please Input To_email:\n")
	return (email_host,from_email,to_email,password)

#Reseive Information
def receiveInfo():
	email_host = raw_input("Please Input Your Email_host:\n")
	email      = raw_input("Please Input Your Email:\n")
	password   = raw_input("Please Input Your Password:\n")
	return (email_host,email,password)

#Connect Send Server
def connSendServer(email_host):
	try:
		smtpObj = smtplib.SMTP(email_host)
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

#Sned Content
def sendMessage():
	subject = raw_input("Please Input Your Email Subject\n")
	content = raw_input("Please Input Your Email Content:\n")
	return (subject,content)

#quit
def Quit():
	print "Thanks For Your Using ."
	print "You Can Report Bugs to 1106911190@qq.com"
	print "PRESS ANYKEY TO QUIT"
	raw_input()
	sys.exit()

if __name__ == '__main__':  
	workType = sendOrReceive()
	if workType == 1:
		email_host,from_email,to_email,password = sendInfo()
		smtpObj = smtplib.SMTP(email_host)
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



