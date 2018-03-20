## sqlite3

SQLite3 与 MySQL 操作相似，都是关系型数据库，但是 SQLite3 比 MySQL 小型化，轻量化，一般在嵌入式设备中使用的较多。

#### 基本使用

##### 连接数据库

connect(database[, timeout, isolation_level, detect_types, factory])

- database 数据库文件，如果没有也可以保存在内存中， conn = sqlite3.connect(":memory:")
- timeout 超时

##### 获取游标

与 MySQL 数据库操作一致，在 SQLite 中对数据库的操作也是要靠游标来完成的。

```
import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()

# do something ...

cur.close()
conn.close()
```

##### 数据操作

使用 execute 命令来执行 sql 语句，演示一下创建删除表，以及增删改查命令。

```
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

```

#### 高级用法

常用的数据库对象

```


import sqlite3

class Database(object):
    """docstring for Database"""
    def __init__(self, db=":memory:"):
        self.db = db
        try:
            self.conn = sqlite3.connect(self.db)
            self.cur = self.conn.cursor()
        except Exception,e:
            print e

    def exec_(self,query):
        try:
            self.cur.execute(query)
            result = {"code":"00","content":[]}
            for x in self.cur.fetchall():
                if len(x)==1:
                    result["content"].append(x[0])
                else:
                    children = []
                    for y in x:
                        children.append(y)
                    result["content"].append(children)
            return result
        except Exception,e:
            result = {"code":"01","content":tuple(e)}
            return result

    def get(self,table,filed=["*"],option={}):
        try:
            if "*" in filed:
                filed = "*"
            else:
                filed = ",".join(filed)
            conds = ""
            if option.get("where",""):
                where = []
                for key,value in option.get("where").items():
                    where.append("%s='%s'"%(unicode(key),unicode(value)))
                conds += "WHERE "
                conds += " AND ".join(where)
            if option.get("order",""):
                order = ""
                order += " ORDER BY "+ option.get("order")[0]
                if len(option.get("order")) == 2:
                    order += " "+option.get("order")[1]
                conds += order
            if option.get("limit",""):
                limit = ""
                if type(option.get("limit")) == str:
                    limit = " LIMIT "+unicode(option.get("limit"))
                else:
                    limit = " LIMIT " + ",".join(option.get("limit"))
                conds += limit
            return self.exec_("SELECT %s FROM %s %s"%(filed,table,conds))
        except Exception,e:
            return {"code":"02","content":tuple(e)}

    def set(self,table,values,option={}):
        try:
            where = []
            for key,value in option.items():
                where.append("%s='%s'"%(unicode(key),unicode(value)))
            conds = []
            for key,value in values.items():
                conds.append("%s='%s'"%(unicode(key),unicode(value)))
            if len(where):
                return self.exec_("UPDATE %s SET %s WHERE %s"%(table," AND ".join(conds)," AND ".join(where)))
            else:
                return self.exec_("UPDATE %s SET %s "%(table," AND ".join(conds)))
        except Exception,e:
            return {"code":"03","content":tuple(e)}

    def new(self,table,values,option=[]):
        try:
            conds = ""
            for i in values:
                if type(i) == int:
                    conds += " %d,"
                else:
                    conds += " '%s',"
            if option:
                return self.exec_("INSERT INTO %s(%s) VALUES(%s)"%(table," , ".join(option),conds[:-1]%(tuple(values))))
            else:
                return self.exec_("INSERT INTO %s VALUES(%s)"%(table,conds[:-1]%(tuple(values))))
        except Exception,e:
            return {"code":"04","content":tuple(e)}

    def del_(self,table,option={}):
        try:
            where = []
            for key,value in option.items():
                where.append("%s='%s'"%(unicode(key),unicode(value)))
            if where:
                return self.exec_("DELETE FROM %s WHERE %s"%(table," AND ".join(where)))
            else:
                return self.exec_("DELETE FROM %s"%table)
        except Exception,e:
            return {"code":"05","content":tuple(e)}

    def __del__(self):
        try:
            self.conn.commit()
            self.cur.close()
            self.conn.close()
        except Exception,e:
            print e


"""
db = Database()

print db.new("user",[2,'姓名','年龄'])

print db.new("user",[2,'name','year'])

print db.get('user')

print db.set("user",{"name":"baobao"},{"int":2})

print db.get("user",option={"int":2})

print db.del_("user",{"int":1})
"""

```
