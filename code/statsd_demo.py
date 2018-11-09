# coding=utf-8
from pystatsd import Client

sc = Client('example.org',8125)

sc.timing('python_test.time',500)
sc.increment('python_test.inc_int')
sc.decrement('python_test.decr_int')
sc.gauge('python_test.gauge', 42)
