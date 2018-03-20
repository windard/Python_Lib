# coding=utf-8

import redis

r = redis.Redis()

r.mset({'country:name': 'China', 'country:location': 'Asia', 'country:area': '960'})

print r.mget({'country:name', 'country:area'})

r.set('school', 'xidian')

print r.get('school')

print r.strlen('school')

print r.substr('school', 0, 3)

r.set('num', 1)

print r.incr('num')

print r.get('num')

print r.incrby('num', 4)

print r.get('num')

print r.decr('num')

print r.get('num')