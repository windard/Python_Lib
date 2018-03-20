# coding=utf-8

import MySQLdb

conn = MySQLdb.Connection(host='127.0.0.1', user='root', passwd='123456', db='test', port=3306, charset='utf8')

with conn as cur:
    
    cur.execute('SELECT * FROM user')

    print 'sum:', cur.rowcount
    
    for row in cur.fetchall():
        print row

