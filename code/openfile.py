#coding=utf-8
filepath = unicode('测试文档.txt','utf8')
file1 = open(filepath,'w')
file1.write("This is for test")
file1.close()
filepath = u'测试文档.txt'
file2 = open(filepath,'r')
print file2.read()
file2.close()