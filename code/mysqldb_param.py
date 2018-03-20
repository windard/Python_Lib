# -*- coding: utf-8 -*-

import MySQLdb

try:
    #打开数据库连接
    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='test')
    print "Connect Successful !"
    #用cursor()获得操作游标
    cur = conn.cursor()

    name = ['windard']

    # 不要这样使用
    cur.execute("SELECT * FROM user WHERE name='%s'" % name[0])
    print cur.fetchone()

    # 这样才是正确的
    cur.execute("SELECT * FROM user WHERE name=%s", name)
    print cur.fetchone()

    # like 的时候是这样
    cur.execute("SELECT * FROM user WHERE name LIKE %s", ['%%%s%%' % name[0]])
    print cur.fetchone()

    conn.close()
except MySQLdb.Error, e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
