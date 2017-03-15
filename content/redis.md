## redis

redis 是一个基于内存的 键值对 存储系统，是NoSQL 的两大代表之一，另一个是 mongoDB 。它不仅能做数据库，还能做缓存，消息代理等，它支持的数据结构有 字符串, 列表, 集合, 字典, 散列, 有序集合, 位图, 地理位置，等多种数据结构，同时它的数据存储在内存中，也可以持久化到硬盘。

常见的五种数据结构与 Python 中的数据结构的对应 字符串 == 字符串 (String), 列表 == 列表 (List), 集合 == 集合 (Set), 散列 == 字典 (Dict), 有序集合 == 有序字典 (Dict), 在 Python 中没有 有序集合 的概念，因为 Python 的字典就是有序的。

redis 的 服务器端是 `redis-server` ，客户端是 `redis-cli`。

一般常用的命令有 `set [key] [value]`, `get [key]`, ,`del [key]`, `keys *` 等。

### 基础使用

- `redis.Redis(self, host='localhost', port=6379, db=0, password=None, socket_timeout=None, socket_connect_timeout=None, socket_keepalive=None, socket_keepalive_options=None, connection_pool=None, unix_socket_path=None, encoding='utf-8', encoding_errors='strict', charset=None, errors=None, decode_responses=False, retry_on_timeout=False, ssl=False, ssl_keyfile=None, ssl_certfile=None, ssl_cert_reqs=None, ssl_ca_certs=None, max_connections=None)` 连接数据库
- `redis.Redis.set(self, name, value, ex=None, px=None, nx=False, xx=False)`  在数据库中增加键值对
- `redis.Redis.get(self, name)` 从数据库中获得键值对

```
# coding=utf-8

import redis

r = redis.Redis()

r.set('name', 'windard')

print r.get('name'), type(r.get('name'))

r.set('windard_infomation', {'name': 'windard', 'year': 21, 'school': 'xidian'})

print r.get('windard_infomation'), type(r.get('windard_infomation'))

r.set('num', [7, 8, 9, 10])

print r.get('num'), type(r.get('num'))
```

输出

```
windard <type 'str'>
{'school': 'xidian', 'name': 'windard', 'year': 21} <type 'str'>
[7, 8, 9, 10] <type 'str'>
```

... 为什么跟我想象的不一样，数组和字典，输出都是 字符串 结构的吖，难道还要自行转换一下。

### 使用列表

注意，在再次使用中设置一个已有键的值，如果两次设置的值的数据类型不一致，会报错 `redis.exceptions.ResponseError: WRONGTYPE Operation against a key holding the wrong kind of value`

可以尽量不要使用同一个键，或者在再次使用中删除该键值对。

- `redis.Redis.lpush(self, name, *values)` 往某个键中填入列表
- `redis.Redis.lpop(self, name)` 从某个键中取出值
- `redis.Redis.lrange(self, name, start, end)` 从某个键取出某些值

```
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
```

输出

```
['1', '9'] <type 'list'>
['9', '1', '1', '9'] <type 'list'>
```

这才是我们想要的列表类型，对列表类型的操作都是以栈的形式进行的。

- `redis.Redis.lindex(self, name, index)`
- `redis.Redis.ltrim(self, name, start, end)`
- `redis.Redis.llen(self, name)`

```
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
```

有几点需注意：
- 虽然我们推进去的是列表，但是每个列表的值，本来是数字，结果还是逃不掉变成字符串的命运
- 若要一次推入多个数值，需要使用 `*[list]` ，而不是直接推入数组，否则也是字符串
- 只有 `push` 和 `pop` 有左边，有右边操作，可以双边操作，其他的 `index`, `range`, `trim` 等都只有左边

### 使用集合

在 Python 中，集合与列表的区别就是 不能有重复的值 ，在 redis 同理。

```

```

### 使用字典

- `redis.Redis.hset(self, name, key, value)`
- `redis.Redis.hget(self, name, key)`
- `redis.Redis.hmset(self, name, mapping)`
- `redis.Redis.hmget(self, name, keys, *args)`
- `redis.Redis.hgetall(self, name)`
- `redis.Redis.hscan(self, name, cursor=0, match=None, count=None)`
- `redis.Redis.hdel(self, name, *keys)`
- `redis.Redis.hkeys(self, name)`
- `redis.Redis.hvals(self, name)`

```
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

# 扫描全部键值对
print r.hscan('school')

# 删除字典的某个键值对
r.hdel('school', 'name')

print r.hgetall('school'), type(r.hgetall('school'))

# 字典的长度
print r.hlen('school')

# 字典的所有键
print r.hkeys('school')

#字典的所有值
print r.hvals('school')

```

输出

```
xidian
['xidian', '86'] <type 'list'>
{'year': '86', 'name': 'xidian', 'location': 'Shannxi'} <type 'dict'>
(0L, {'year': '86', 'name': 'xidian', 'location': 'Shannxi'})
{'location': 'Shannxi', 'year': '86'} <type 'dict'>
2
['location', 'year']
['Shannxi', '86']
```

### 高级使用

redis 也是有不同的库 (database) 的，默认是使用 0 号库，切换数据库是 `select [tablenum]` 

删除当前库所有键值对是 `flushdb`, 删除所有库的所有数据 `flushall`

redis 还有一个神奇的特性是可以设置生存时间，默认生存时间为 -1 ，即无穷，在超过生存时间之后即会自动消失。

```
# coding=utf-8

import time
import redis

r = redis.Redis(db=1)

# 查看所有键
print r.keys('*')

# 情况当前数据库
r.flushdb()

print r.keys('*')

# 设置超时时间为 10 秒
r.set('name', 'windard', ex=15)

# 设置超时时间 5 秒
r.set('school', 'xidian')
r.expire('school', 5)

# 对某个键重命名
r.rename('school', 'university')

print r.keys("*")

# 查看某个键值对的类型或者值
r.type('name')

# 随机获得一个键名
print r.randomkey()

# 查看某个键的剩余超时时间
print r.ttl('university')

time.sleep(5)

# 查看某个键值对是否还存在
r.exists('university')

# 将某个键值对持久化
r.persist('name')

print r.exists('name')
print r.ttl('name')

# 将数据移到另一个数据库
r.move('name', 0)

print r.exists('name')
```

输出 

```
['name']
[]
['university', 'name']
university
5
True
None
False
```

### 其他应用


