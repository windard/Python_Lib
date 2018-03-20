# coding=utf-8

import MySQLdb

try:
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123456', db='test', port=3306, charset='utf8')

    # 数据库连接信息
    print "Host Info  :", conn.get_host_info()
    print "Server Info:", conn.get_server_info()

    conn.query('SELECT * FROM user')

    # fetch_row 默认只取一条数据
    for row in conn.use_result().fetch_row(10):
        print row

except MySQLdb.Error,e:
     print "MySQL Error %d: %s" % tuple(e)
else:
    conn.close()
