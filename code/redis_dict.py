# coding=utf-8

import redis

r = redis.Redis()

r.delete('school')

# 在一个键值对中设置一个键值对
r.hset('school', 'name', 'xidian')

print r.hget('school', 'name')

# 在一个键值对中设置多个键值对
r.hmset('school', {'year': 86, 'location': 'Shannxi'})

# 一次获得多个键的值
print r.hmget('school', ['name', 'year']), type(r.hmget('school', ['name', 'year']))

# 一次获得全部的键值对
print r.hgetall('school'), type(r.hgetall('school'))

# 删除字典的某个键值对
r.hdel('school', 'name')

print r.hgetall('school'), type(r.hgetall('school'))

# 字典的长度
print r.hlen('school')

# 字典的所有键
print r.hkeys('school')

#字典的所有值
print r.hvals('school')
