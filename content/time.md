## time

时间函数time，使用起来也非常简单，一般用来取得当前时间，和计算一段时间差。

```
time() -- return current time in seconds since the Epoch as a float
clock() -- return CPU time since process start as a float
sleep() -- delay for a number of seconds given as a float
gmtime() -- convert seconds since Epoch to UTC tuple
localtime() -- convert seconds since Epoch to local time tuple
asctime() -- convert time tuple to string
ctime() -- convert time in seconds to string
mktime() -- convert local time tuple to seconds since Epoch
strftime() -- convert time tuple to string according to format specification
strptime() -- parse string to time tuple according to format specification
tzset() -- change the local timezone
```

输出当前时间

```python

import time

print "Time:%s\n" % time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())

print time.strftime('%Y-%m-%d %H:%M:%S')

```

```
Time:2016-09-29 11:46:53
2016-09-29 11:46:53
```

时间格式

- %a 星期几的简写
- %A 星期几的全称
- %b 月分的简写
- %B 月份的全称
- %c 标准的日期的时间串
- %C 年份的前两位数字
- %d 日期，不足不补零
- %D 月/天/年
- %e 日期，不足即补零
- %F 年-月-日
- %g 年份的后两位数字
- %G 完整的年份
- %h 简写的月份名
- %H 24小时制的小时
- %I 12小时制的小时
- %j 十进制表示的每年的第几天
- %m 十进制表示的月份
- %M 十时制表示的分钟数
- %n 新行符，换行符
- %p 本地的AM或PM的等价显示
- %r 12小时的时间
- %R 显示小时和分钟：hh:mm
- %S 十进制的秒数
- %t 水平制表符
- %T 显示时分秒：hh:mm:ss
- %u 每周的第几天，星期一为第一天(1-7)
- %U 第年的第几周，把星期日做为第一天（值从0到53）
- %V 每年的第几周，使用基于周的年
- %w 每周的第几天，星期天为第0天(0-6)
- %W 每年的第几周，把星期一做为第一天（值从0到53）
- %x 标准的日期串
- %X 标准的时间串
- %y 不带世纪的十进制年份（值从0到99）
- %Y 带世纪部分的十制年份
- %z，%Z 时区名称，如果不能得到时区名称则返回空字符。
- %% 百分号

时间格式转换

```
from time import ctime
from datetime import datetime
print datetime.strptime(ctime(), '%a %b %d %H:%M:%S %Y').strftime('%Y-%m-%d %H:%M:%S')
```

```
2016-09-29 11:49:05
```

获得时分秒

```python

import time
import calendar

# 显示从1970年1月1日到现在经过了多长时间
print time.time()
#延迟3秒
time.sleep(3)
print time.time()

#显示当前时间
print time.ctime()
#time.ctime(t) 显示从1970年1月1日过了t秒钟的时间


#或者这样
print time.asctime( time.localtime(time.time()) )

#详细的时间参数
print "This year is :     " + str(time.localtime(time.time()).tm_year)
print "This month is :    " + str(time.localtime(time.time()).tm_mon)
print "This day is :      " + str(time.localtime(time.time()).tm_mday)
print "This hour is :     " + str(time.localtime(time.time()).tm_hour)
print "This minute is :   " + str(time.localtime(time.time()).tm_min)
print "This second is :   " + str(time.localtime(time.time()).tm_sec)
print "This weekday is :  " + str(time.localtime(time.time()).tm_wday)
print "This year day is : " + str(time.localtime(time.time()).tm_yday)

#获取某月日历
print calendar.month(2008, 1)
```

保存为time_demo.py，运行，看一下效果。

![time_demo.jpg](images/time_demo.jpg)

计算时间差。

```python
import time

start_time = time.clock()
time.sleep(3)
end_time   = time.clock()
print "%.4f second"%(end_time - start_time)
```

保存为time_time.py，运行，看一下结果。

![time_time.jpg](images/time_time.jpg)

可以看到每次执行的时间都不一样，但是都在3秒左右。

> 但是在 Mac 上非常神奇的是，可能是多核 CPU 的原因，不准！！！

## 一点补充

原来在 Linux/Unix 平台上都不准，`time.clock` ,只有在 Windows 上才能使用，在其他平台上还是老老实实使用 `time.time`.

或者自己实现 `default_timer`

```
if sys.platform == "win32":
    # On Windows, the best timer is time.clock()
    default_timer = time.clock
else:
    # On most other platforms the best timer is time.time()
    default_timer = time.time
```
