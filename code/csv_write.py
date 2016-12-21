# coding: utf-8

import csv

# 若不用 b 的话，在每一行的后面会空一行
csvfile = file('csv_test.csv', 'wb')
writer = csv.writer(csvfile)

# 写入单行数据
writer.writerow(['year', 'month', 'day'])

data = [
    ('2017', '1', '26'),
    ('2017', '1', '27')
]

# 写入多行数据
writer.writerows(data)

csvfile.close()