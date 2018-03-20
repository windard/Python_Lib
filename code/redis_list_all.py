# coding=utf-8

import redis

r = redis.Redis()

r.delete('num')

# 一次填充多个数值
r.rpush('num', *[1, 6, 9])

# 从另一个方向填值, 这样填入就会被当成字符串
r.lpush('num', [3, 2, 1])

result = r.lrange('num', 0, -1)
print result, type(result)

# 从左边索引到 序号为3 的值

index = r.lindex('num', 3)
print index

# 对列表进行修剪，将第一个去掉
r.ltrim('num', 1, -1)

result = r.lrange('num', 0, -1)
print result, type(result)

# pop 最左边的元素

print r.lpop('num')

# pop 最右边的元素

print r.rpop('num')

result = r.lrange('num', 0, -1)
print result, type(result)