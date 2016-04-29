#coding=utf-8

import re

pattern = re.compile(r"(\w{1,6})(\s)(\,)(\s)(\w*)$")
m = re.match(pattern,"hello , world")

print "m.string:", m.string
print "m.re:", m.re
print "m.re.pattern:", m.re.pattern
print "m.pos:", m.pos
print "m.endpos:", m.endpos
print "m.lastindex:", m.lastindex
print "m.lastgroup:", m.lastgroup

print "m.group():", m.group()
print "m.group(1,2):", m.group(1, 2)
print "m.groups():", m.groups()
print "m.groupdict():", m.groupdict()
print "m.start(2):", m.start(2)
print "m.end(2):", m.end(2)
print "m.span(2):", m.span(2)
