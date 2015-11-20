#coding=utf-8
import sys

print sys.version
print sys.version_info
print sys.hexversion
print sys.api_version
print sys.exec_prefix 
print sys.executable
print sys.maxint
print sys.maxunicode
print sys.byteorder
print sys.getdefaultencoding()
print sys.getwindowsversion()
print sys.getfilesystemencoding()
modules =  sys.modules
for i in modules.keys():
	print i
print sys.copyright

