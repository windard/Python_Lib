## pymysql

虽然在 Python 中有一个 MySQLdb 的官方依赖库，但是它是 C语言写的，有一些 C相关的依赖不太好装，而且也不够 pythonic ，一般用 pymysql 会比较方便。

首先，安装就很简单

```
pip install pymysql
```

### 使用示例

使用 pymysql 文档中提供的数据库表字段

```
CREATE TABLE `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `email` varchar(255) COLLATE utf8_bin NOT NULL,
    `password` varchar(255) COLLATE utf8_bin NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
AUTO_INCREMENT=1 ;
```

**需要注意的是，SQL 语句中的占位符，只能是用 `%s` 或者 `%(name)s`**


```
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

```

