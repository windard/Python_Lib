# coding=utf-8

from collections import deque

d = deque()

d.append(1)
d.append(2)
d.appendleft(3)
d.appendleft(4)

print d

print d.pop()
print d.popleft()

print d[0]
print d[-1]

l = deque(maxlen=5)
l.extend(range(5))

print l, len(l)

l.extendleft([6])

print l, len(l)

l.rotate(2)
print l

l.rotate(-3)
print l

l.reverse()
print l
