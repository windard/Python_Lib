# coding=utf-8

import redis

r = redis.Redis()

r.delete('num')

# 填入一个值
r.rpush('num', 1)

r.rpush('num', 9)

# 索引从第一个到最后一个的值
result = r.lrange('num', 0, -1)

print result, type(result)

# 从另一个方向填值
r.lpush('num', 1)

r.lpush('num', 9)

result = r.lrange('num', 0, -1)

print result, type(result)