# coding=utf-8

import sqlite3

conn = sqlite3.connect(":memory:")

cur = conn.cursor()

# 创建一个表单

sql = "CREATE TABLE test(id int primary key,name varchar(20),email varchar(30));"

try:
	cur.execute(sql)
	conn.commit()
except Exception,e:
	print "Create Failed",e

# 增加一条记录

sql_insert = "INSERT INTO test VALUES (1,'windard','windard@windard.com');"

try:
	cur.execute(sql_insert)
	conn.commit()
except Exception, e:
	print "Insert Failed",e

# 修改一条记录

sql_update = "UPDATE test SET name='admin',email='me@windard.com' WHERE id=1;"

try:
	cur.execute(sql_update)
	conn.commit()
except Exception, e:
	print "Update Failed",e

# 查找数据

sql_select = "SELECT * FROM test;"

try:
	cur.execute(sql_select)
	# 一次获得一条数据
	result = cur.fetchone()
	print result
	# 一次获得多条数据
	result = cur.fetchall()
	for x in result:
		print x
except Exception,e:
	print "Select Failed",e

# 删除数据


sql_delete = "DELETE FROM test WHERE id=1"

try:
	cur.execute(sql_delete)
	conn.commit()
except Exception, e:
	print "Delete Failed",e

cur.close()
conn.close()
