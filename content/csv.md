## csv

csv 也是一种数据格式化的标准，全称为 `Comma Separated Values` ,意为用逗号分隔的数据。

### 写入

```
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
```

写入效果

```
year,month,day
2017,1,26
2017,1,27
```

## 读取

```
# coding: utf-8

import csv

csvfile = file('csv_test.csv', 'rb')
reader = csv.reader(csvfile)

for line in reader:
	print line
	if reader.line_num != 1:
		print line[0]

csvfile.close()

```

读取效果

```
['year', 'month', 'day']
['2017', '1', '26']
2017
['2017', '1', '27']
2017
```