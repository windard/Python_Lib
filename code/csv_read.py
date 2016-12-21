# coding: utf-8

import csv

csvfile = file('csv_test.csv', 'rb')
reader = csv.reader(csvfile)

for line in reader:
	print line
	if reader.line_num != 1:
		print line[0]

csvfile.close()

