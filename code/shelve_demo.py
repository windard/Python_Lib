# -*- coding: utf-8 -*-
# # coding=utf-8

# import shelve

# s = shelve.open('test.dat')

# s['x'] = ['a', 1, [2, 'b']]

# s['x'].append('d')

# print s['x']

# # coding=utf-8

# import shelve

# s = shelve.open('test.dat')

# s['x'] = ['a', 1, [2, 'b']]

# temp = s['x']

# temp.append('d')

# s['x'] = temp

# print s['x']


# coding=utf-8

import shelve

s = shelve.open('test.dat', writeback=True)

s['x'] = ['a', 1, [2, 'b']]

s['x'].append('d')

print s['x']
