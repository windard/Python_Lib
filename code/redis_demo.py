# coding=utf-8

import redis

r = redis.Redis()

r.set('name', 'windard')

print r.get('name'), type(r.get('name'))

r.set('windard_infomation', {'name': 'windard', 'year': 21, 'school': 'xidian'})

print r.get('windard_infomation'), type(r.get('windard_infomation'))

r.set('num', [7, 8, 9, 10])

print r.get('num'), type(r.get('num'))