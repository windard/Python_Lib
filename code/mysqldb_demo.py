#coding=utf-8
import MySQLdb

try:
	#打开数据库连接
	conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='test',port=3406)
	print "Connect Successful !"
	#用cursor()获得操作游标
	cur = conn.cursor()
	#使用execute()执行SQL语句
	cur.execute("SELECT VERSION()")
	#使用fetchone()获得一条数据库
	data = cur.fetchone()
	print "Datebase Version : %s" %data 
	conn.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])