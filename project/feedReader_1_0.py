#coding=utf-8

import smtplib
import MySQLdb
import feedparser
from email.mime.text import MIMEText
from datetime import datetime

FEED_URL = 'http://1418019.top/rss.xml'
HOST = "smtp.163.com"
from_name = '18607571914@163.com'
to_name = 'me@wenqiangyang.com'
password = 'XXXXXX'

def checkMySQL(conn,entry):
	cur = conn.cursor()
	cur.execute('SET NAMES utf8;')
	cur.execute('SET CHARACTER SET utf8;')
	cur.execute('SET character_set_connection=utf8;')		
	cur.execute("SELECT * FROM homework WHERE title=%s AND content=%s",(entry.title,entry.description))
	data = cur.fetchone()
	cur.close()
	if data == None:
		return 0
	else:
		return 1

def writeMySQL(conn,entry):
	cur = conn.cursor()
	cur.execute('SET NAMES utf8;')
	cur.execute('SET CHARACTER SET utf8;')
	cur.execute('SET character_set_connection=utf8;')			
	cur.execute("INSERT INTO homework(title,link,published,content) VALUES(%s,%s,%s,%s)",(entry.title,entry.link,entry.published,entry.description))
	conn.commit()
	cur.close()

def writeDown(log,desc):
	log.write(str(datetime.now())+":    "+desc+"\n")

if __name__ == '__main__':
	content=""
	log = open('/home/windard/Document/feed/feed.log','a')
	writeDown(log,"Starting Python Script")
	try:
		conn = MySQLdb.connect(host='localhost',user='root',passwd='XXXXXX',db='feed',port=3406)
		conn.set_character_set('utf8')
		writeDown(log,"Connecting to MySQL Successful")
	except MySQLdb.Error,e:
	 	writeDown(log,"Connecting to MySQL Failed  %s" %e.args[1])	
	else:
		try:
			data = feedparser.parse(FEED_URL)
		except feedparser.Error,e:
			writeDown(log,"Connecting to Feed Failed %s" %e.args[1])
		else:
			writeDown(log,"Receiving Feed Successful")
			flag = 0
			for entry in data.entries:
				if checkMySQL(conn,entry):
					pass
				else:
					writeMySQL(conn,entry)
					writeDown(log,"One Article is new")
					content +="<a href =\""+entry.link+"\" >"+"<h1>"+entry.title+"</h1>"+"</a>"
					content += entry.description
					content += "<br />"			
					flag = 1
			if flag :
				smtpObj = smtplib.SMTP(HOST)
				message = MIMEText(content,_subtype='html',_charset='utf-8')
				message["Subject"] = data.feed.title
				message["From"] = from_name
				message["To"] = to_name
				try:
					smtpObj.login(from_name,password)
					writeDown(log,"Connecting to Mail Successful")
				except smtplib.e:
					writeDown(log,"Connecting to Mail Failed %s" %e.args[1])
				else:
					smtpObj.sendmail(from_name,to_name,message.as_string())
					writeDown(log,"Sending Successful")
					smtpObj.close()	
			else :
				writeDown(log,"Today is nothing new")

		finally:
			conn.close()
	finally:
		writeDown(log,"Ending Python Script")
		log.close()