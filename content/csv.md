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

这样的写入效果不太好，只能写入大量的同类型数据而没有标题。

```
# coding=utf-8
import csv

headers = ['Symbol', 'Price', 'Date', 'Time', 'Change', 'Volume']
rows = [{'Symbol':'AA', 'Price':39.48, 'Date':'6/11/2007',
        'Time':'9:36am', 'Change':-0.18, 'Volume':181800},
        {'Symbol':'AIG', 'Price': 71.38, 'Date':'6/11/2007',
        'Time':'9:36am', 'Change':-0.15, 'Volume': 195500},
        {'Symbol':'AXP', 'Price': 62.58, 'Date':'6/11/2007',
        'Time':'9:36am', 'Change':-0.46, 'Volume': 935000},
        ]

with open('stocks.csv','w') as f:
    f_csv = csv.DictWriter(f, headers)
    f_csv.writeheader()
    f_csv.writerows(rows)

```

写入效果

```
Symbol,Price,Date,Time,Change,Volume
AA,39.48,6/11/2007,9:36am,-0.18,181800
AIG,71.38,6/11/2007,9:36am,-0.15,195500
AXP,62.58,6/11/2007,9:36am,-0.46,935000

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