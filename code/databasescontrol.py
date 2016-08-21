#coding=utf-8

import MySQLdb

class Database(object):
    """docstring for Database"""
    def __init__(self, host="localhost",user="root",password="",db="",port=3406,charset="utf8"):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.charset = charset
        self.db = db
        try:
            self.conn = MySQLdb.connect(host=self.host,user=self.user,passwd=self.password,db=self.db,port=self.port,charset=self.charset)
            self.conn.set_character_set('utf8')
            self.cur = self.conn.cursor()
            self.cur.execute('SET NAMES utf8;')
            self.cur.execute('SET CHARACTER SET utf8;')
            self.cur.execute('SET character_set_connection=utf8;')
        except Exception,e:
            print e

    def exec_(self,query):
        try:
            print query
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
                    where.append("%s='%s'"%(str(key),str(value)))
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
                    limit = " LIMIT "+str(option.get("limit"))
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
                where.append("%s='%s'"%(str(key),str(value)))
            conds = []
            for key,value in values.items():
                conds.append("%s='%s'"%(str(key),str(value)))
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
                where.append("%s='%s'"%(str(key),str(value)))
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

import databasescontrol

a = databasescontrol.Database(password="123456")

print a.exec_("show databases")

print a.exec_("use test")

# print a.get("user",option={"where":{"password":"haha"},"limit":["2","2"],"order":["id","DESC"]})
# print a.set("user",{"username":"wocao"})

print a.new("user",["name","password"],["username","password"])

# print a.del_("user")

print a.get("user")

"""
