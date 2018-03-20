# coding=utf-8

import redis

r = redis.Redis()

r.delete('name')

r.sadd('name', 'mary', 'heny')

r.sadd('name', 'john', 'anny')

print r.smembers('name')

# 查看集合中值的数量
print r.scard('name')

print r.sismember('name', 'john')

print r.sismember('name', 'venr')
