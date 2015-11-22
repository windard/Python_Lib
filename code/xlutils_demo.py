#coding=utf-8
from xlrd import open_workbook
from xlutils.copy import copy
 
 #打开表单时，保留原有表单格式
rb = open_workbook('test.xls',formatting_info=True)
 
#通过sheet_by_index()获取的sheet没有write()方法
rs = rb.sheet_by_index(0)

wb = copy(rb)
 
#通过get_sheet()获取的sheet有write()方法
ws = wb.get_sheet(0)
ws.write(0, 0, 'changed!')
 
wb.save('test.xls')