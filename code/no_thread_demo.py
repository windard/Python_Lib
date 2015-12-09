#coding=utf-8

from time import ctime,sleep

def loop0():
	print 	"loop0 start at: ",ctime()
	sleep(2)
	print 	"loop0 end 	 at: ",ctime()

def loop1():
	print 	"loop1 start at: ",ctime()
	sleep(4)
	print 	"loop1 end 	 at: ",ctime()

print "all start at: ",ctime()
loop0()
loop1()
print "all end   at: ",ctime()