#coding=utf-8
import MySQLdb

try:
	conn = MySQLdb.connect(host='localhost',user='root',passwd='',port=3406,charset='utf8')
	print "Connect Successful !"
	cur = conn.cursor()
	#创建一个新的数据库名为python
	cur.execute("CREATE DATABASE IF NOT EXISTS python")
	#连接这个数据库
	conn.select_db('python')
	#创建一个新的表单test
	cur.execute("CREATE TABLE test(id int,info varchar(20))")
	#插入单个数据
	value = [1,'windard']
	cur.execute("INSERT INTO test VALUES(%s,%s)",value)
	conn.commit()
	#查看结果
	cur.execute("SELECT * FROM test ")
	data = cur.fetchone()
	print data
	#插入大量数据	
	values = []
	for i in range(20):
		values.append((i,'this is number :' + str(i)))
	cur.executemany("INSERT INTO test VALUES(%s,%s)",values)
	conn.commit()	
	#查看结果，此时execute()的返回值是插入数据得到的行数
	print "All Database Table"
	count = cur.execute("SELECT * FROM test ")
	data = cur.fetchmany(count)
	for item in data:
		print item	
	#删除表单
	cur.execute("DROP TABLE test ")
	#删除数据库
	cur.execute("DROP DATABASE python")
	cur.close()
	conn.close()
except MySQLdb.Error,e:
	print "Mysql Error %d: %s" % (e.args[0], e.args[1])

