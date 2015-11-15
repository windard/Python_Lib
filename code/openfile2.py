#coding=utf-8
filepath = unicode('测试文档.txt','utf8')
file1 = open(filepath,'w')
file1.write('这是测试文档')
file1.close()
filepath = u'测试文档.txt'
file2 = open(filepath,'r','utf-8')
print file2.read()
# print file2.read().decode('utf8')
file2.close()