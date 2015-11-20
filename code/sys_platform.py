#coding=utf-8
import sys
print sys.platform
path = sys.path
for i in path:
	print i
sys.exit(0)
print "This won't run"