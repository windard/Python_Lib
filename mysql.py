#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb

# 打开数据库连接
db = MySQLdb.connect(host = "http://pma.tools.sinaapp.com/index.php?db=app_tablegather&v=5847699948912508928",user = "SAE_MYSQL_USER", passwd = "SAE_MYSQL_PASS",db = "jiaowuchu")
if db:
	print "Successful"
else:
	print "Error "
# 使用cursor()方法获取操作游标 
# cursor = db.cursor()
# value=['1','hi rollen','34','asvd']
# if cursor.execute('INSERT INTO name(name,id,something,otherthing) values(%s,%s,%s,%s)',value):
# 	print 'Successful '
# else:
# 	print "Errpr"

# db.commit()
# 使用execute方法执行SQL语句
# cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取一条数据库。
# data = cursor.fetchone()

# print "Database version : %s " % data

# 关闭数据库连接
db.close()