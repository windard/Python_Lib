#coding=gbk
import xlwt


excel = xlwt.Workbook("test.xls")


table = excel.add_sheet("sheet_one")
table.write(0,0,"test")


excel.save('test.xls')