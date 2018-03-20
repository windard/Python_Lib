# coding=utf-8

import redis

r = redis.Redis()

r.delete('name')

# mary 的分数是 1.1
# lily 的分数是 3.3
# john 的分数是 2.2
# heny 的分数是 4.4
r.zadd('name', 'mary', 1.1, 'lily', 3.3, john=2.2, heny=4.4)

# 查看所有元素
print r.zrange('name', 0, -1)

# 查看某个元素的位置
print r.zrank('name', 'lily')

# 查看所有元素，并显示分数
print r.zrange('name', 0, -1, True)

# 查看分数在 2-4 之间的元素
print r.zrangebyscore('name', 2, 4)

# 计数，统计所有元素的数量
print r.zcard('name')

# 计数，统计分数在 0-3 之间的数目
print r.zcount('name', 0, 3)

# 删除元素
r.zrem('name', 'mary')

print r.zrange('name', 0, -1)

# 通过索引删除元素
r.zremrangebyrank('name', 0, 1)

print r.zrange('name', 0, -1)

# 通过分数删除元素
r.zremrangebyscore('name', 1, 2)

print r.zrange('name', 0, -1)
