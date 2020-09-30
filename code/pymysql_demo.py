# -*- coding: utf-8 -*-

import pymysql


connection = pymysql.connect(host='localhost',
                             user='user',
                             password='passwd',
                             db='db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
    sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
    # 插入单行数据
    cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
    # 插入多行数据
    cursor.executemany(sql, [
        ('developer@python.org', 'medium-secret'),
        ('support@python.org', 'low-secret')
    ])

try:
    connection.commit()
except Exception as e:
    print(repr(e))
    connection.rollback()

with connection.cursor() as cursor:
    sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
    cursor.execute(sql, ('webmaster@python.org',))
    result = cursor.fetchone()
    print(result)
    # 使用 DictCursor 可以将 fetch 到的结果转化成 dict 格式
    print(result['id'])

    sql = "SELECT * from users;"
    cursor.execute(sql)
    result = cursor.fetchall()
    print([d['email'] for d in result])

# 最后别忘了关闭连接
connection.close()
