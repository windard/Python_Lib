#coding=utf-8

import zipfile

filename = 'glob_demo.py'

zipname = zipfile.ZipFile('glob_demo.zip','w',zipfile.ZIP_DEFLATED)
zipname.write(filename)
zipname.close()
