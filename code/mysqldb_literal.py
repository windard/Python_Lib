# coding=utf-8

import MySQLdb

conn = MySQLdb.Connection(host='127.0.0.1', user='root', passwd='123456', db='test', port=3306, charset='utf8')

print conn.literal(["0 or 1=1; # -- ", 'windard'])

print conn.literal("0' or 1=1; # -- ")