## datetime

datetime 和 timestamp(int) 的相互转换，在时间处理的时候，见到的最多的时间表示方式就是这两者了，时间的表示格式既可以使用 timestamp ，也可以选择使用 datetime 或者是 struct_time ，但是在数据库中一般常见的是是用 integer 或者 datetime 这两种类型存储，那么这三者的转换关系呢？

> datatime 之间混乱的关系终于有人能出来解决一下，requests 作者 Kennethreitz 的 [Maya: Datetimes for Humans™](https://github.com/kennethreitz/maya) 可以看一看

### 时间的几种表现形式

UTC (Coordinated Universal Time) 是一种时间标准，以 1970年1月1日0时0分0秒的格林尼治时间为起点的时间计量标准，这一时间点也被称为 普朗克时间 (epoch time)。该标准将全世界分为 24 个时区，中国位于 UTC+8 的时区之内。现在全世界的计算机时间也都是采用这一标准。

常用的时区 GMT(Greenwich Mean Time) 格林尼治时间， CST(China Standard Time) 中国标准时间。

#### ISO 8601

ISO 8601的标准格式是：`YYYY-MM-DDTHH:mm:ss.sssZ`

- `YYYY`：年份，0000 ~ 9999
- `MM`：月份，01 ~ 12
- `DD`：日，01 ~ 31
- `T`：分隔日期和时间，可以使用 `T` 或者空格。
- `HH`：小时，00 ~ 24
- `mm`：分钟，00 ~ 59
- `ss`：秒，00 ~ 59
- `.sss`：毫秒
- `Z`：时区，可以是：Z(格林尼治时间)、+HH:mm、-HH:mm

这是最常见的时间写法,如 `2017-08-27T15:18:47.364Z`，一般也简写为 `YYYY-MM-DD HH:mm:ss` 如 `2017-08-27 10:23:21`

#### RFC-2822

RFC-2822 的标准格式是: `(Week) (Month) DD YYYY HH:mm:ss Z` 如 `Sun Aug 27 2017 23:22:10 GMT+0800 (CST)`

- Week :  "Mon" / "Tue" / "Wed" / "Thu" / "Fri" / "Sat" / "Sun"
- Month : "Jan" / "Feb" / "Mar" / "Apr" / "May" / "Jun" / "Jul" / "Aug" / "Sep" / "Oct" / "Nov" / "Dec"

#### 时间戳

时间戳一般就是指的格林尼治时间，不加时区的，不会造成歧义，其他的时间表示形式都需要加时区。在 Linux 下使用 `date +%s` 可以查看到当前的时间戳,时间戳一般计算到秒级，可以使用整数表示，也可以计算到毫秒级甚至纳秒级，用浮点数表示。


### datetime 的简单使用

```
datetime.datetime.now()
datetime.datetime.now().weekday()
datetime.datetime.now().isoweekday()
```

### 时间制式的不同表达

在 Python 中有两个与时间处理相关的库，一个是 `time` 另一个是 `datetime` 。 在 Python 的时间的格式有 `time.struct_time` 和 `datetime.datetime` 还有直接使用 int 表示的 timestamp 。

使用 time

```
# coding=utf-8

import time

# timestamp
print time.time()
print int(time.time())

# ISO 8601
print time.strftime('%F %T%z (%Z)')
print time.strftime('%Y-%m-%d %H:%M:%S')

# RFC-2822
print time.strftime('%c')
print time.asctime()
print time.ctime()

# time.struct_time
print time.localtime()

```

输出为

```
1503847989.54
1503847989
2017-08-27 23:33:09+0800 (CST)
2017-08-27 23:33:09
Sun Aug 27 23:33:09 2017
Sun Aug 27 23:33:09 2017
Sun Aug 27 23:33:09 2017
time.struct_time(tm_year=2017, tm_mon=8, tm_mday=27, tm_hour=23, tm_min=33, tm_sec=9, tm_wday=6, tm_yday=239, tm_isdst=0)
```

使用 datetime

> 使用 datetime 有一个非常坑的地方，使用 `now()` 和 `utcnow()` 获得的时间的结果的表示格式是一致的，也就是说不能从时间格式中读取时区信息，如果使用双方沟通不一致的话，容易出现时区混乱的问题。
> 所有有 `fromtimestamp` 和 `utcfromtimestamp`

```
# coding=utf-8

from datetime import datetime

# ISO 8601
print datetime.now()
print datetime.utcnow()

format(datetime.datetime.now(), "%Y-%m-%d %H:%M")

```

输出为

```
2017-10-22 23:38:28.937915
2017-10-22 15:38:28.937953
```

### 时间格式的转换

```
# coding=utf-8

import time
from datetime import datetime


def timestamp_to_strtime(timestamp):
    """将 11 位整数的毫秒时间戳转化成本地普通时间 (字符串格式)
    :param timestamp: 11 位整数的毫秒时间戳 (1456402864)
    :return: 返回字符串格式 {str}'2016-02-25 20:21:04.000000'
    """
    local_str_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return local_str_time


def timestamp_to_datetime(timestamp):
    """将 11 位整数的毫秒时间戳转化成本地普通时间 (datetime 格式)
    :param timestamp: 11 位整数的毫秒时间戳 (1456402864)
    :return: 返回 datetime 格式 {datetime}2016-02-25 20:21:04.000000
    """
    local_dt_time = datetime.fromtimestamp(timestamp)
    return local_dt_time


def datetime_to_strtime(datetime_obj):
    """将 datetime 格式的时间 (含毫秒) 转为字符串格式
    :param datetime_obj: {datetime}2016-02-25 20:21:04.000000
    :return: {str}'2016-02-25 20:21:04.242'
    """
    # return datetime_obj.isoformat()
    local_str_time = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    return local_str_time


def datetime_to_timestamp(datetime_obj):
    """将本地(local) datetime 格式的时间 (含毫秒) 转为毫秒时间戳
    :param datetime_obj: {datetime}2016-02-25 20:21:04.000000
    :return: 11 位的毫秒时间戳  1456402864
    """
    local_timestamp = int(time.mktime(datetime_obj.timetuple()))
    return local_timestamp


def strtime_to_datetime(timestr):
    """将字符串格式的时间 (含毫秒) 转为 datetime 格式
    :param timestr: {str}'2016-02-25 20:21:04'
    :return: {datetime}2016-02-25 20:21:04.000000
    """
    local_datetime = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
    return local_datetime


def strtime_to_timestamp(local_timestr):
    """将本地时间 (字符串格式，含毫秒) 转为 11 位整数的毫秒时间戳
    :param local_timestr: {str}'2016-02-25 20:21:04'
    :return: 1456402864
    """
    local_datetime = strtime_to_datetime(local_timestr)
    timestamp = datetime_to_timestamp(local_datetime)
    return timestamp


print timestamp_to_strtime(time.time())
print datetime_to_timestamp(datetime.now())
print strtime_to_timestamp('2017-08-27 23:52:39')
```

更优雅的将 datetime.datetime 转换为 timestamp

```
# -*- coding: utf-8 -*-

import time
import calendar
import datetime


def datetime_to_timestamp_by_datetime(datetime_obj):
    return int(datetime_obj.strftime("%s"))


def datetime_to_timestamp_by_time(datetime_obj):
    return int(time.mktime(datetime_obj.timetuple()))


def datetime_to_timestamp_by_calender(datetime_obj):
    return int(calendar.timegm(datetime_obj.timetuple()))


def datetime_to_timestamp_by_calculate(datetime_obj):
    return int((datetime_obj - datetime.datetime(1970, 1, 1)).total_seconds())


def main():
    now = datetime.datetime.now()
    print datetime_to_timestamp_by_datetime(now)
    print datetime_to_timestamp_by_time(now)
    print datetime_to_timestamp_by_calender(now)
    print datetime_to_timestamp_by_calculate(now)


if __name__ == '__main__':
    main()

```

### 时间区间的转换

Python 中与时区相关的库 `pytz` ，查看所有的时区 `pytz.all_timezones`,查看中国的时区 `pytz.country_timezones('CN')` 创建一个时区 `pytz.timezone('Asia/Shanghai')`

创建时间的时候默认使用本地时区，也可以指定时区。

> 还有 `tzlocal` 获得当前时区 `tzlocal.get_localzone()`

```
In [13]: import datetime

In [14]: datetime.datetime.now()
Out[14]: datetime.datetime(2017, 9, 7, 14, 22, 27, 743300)

In [15]: tz=pytz.timezone('Asia/Shanghai')

In [16]: datetime.datetime.now(tz)
Out[16]: datetime.datetime(2017, 9, 7, 14, 22, 51, 674551, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>)

In [17]: ut=pytz.timezone('UTC')

In [18]: ut
Out[18]: <UTC>

In [19]: datetime.datetime.now(ut)
Out[19]: datetime.datetime(2017, 9, 7, 6, 23, 38, 608467, tzinfo=<UTC>)
```

转换时区的时候即可以使用 datetime.datetime 的 `astimezone` 函数即可修改时区

```
In [25]: t
Out[25]: datetime.datetime(2017, 9, 7, 6, 26, 24, 857174, tzinfo=<UTC>)

In [26]: t.astimezone(pytz.timezone('Asia/Shanghai'))
Out[26]: datetime.datetime(2017, 9, 7, 14, 26, 24, 857174, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>)

In [27]: t
Out[27]: datetime.datetime(2017, 9, 7, 6, 26, 24, 857174, tzinfo=<UTC>)
```

在 python 3 中还可以使用 timezone 来做时区转换

```

```

### 更好的时间转换

将时间字符串转换为 `datetime.datetime` `parser.parse(iso_str).astimezone(pytz.timezone('Asia/Shanghai'))`

将 `time.struct_time` 转换为时间戳 `calendar.timegm(time.gmtime())`

```
# coding=utf-8

import pytz
import calendar
from dateutil import parser
from datetime import timedelta, datetime


def iso2datetime(iso_str):
    return parser.parse(iso_str)


def datetime2utc(datetime_obj):
    return datetime_obj.astimezone(pytz.timezone('Asia/Shanghai'))


def timestamp():
    return calendar.timegm(time.gmtime())


def timedate_obj():
    return datetime.now()


def ios_str():
    return datetime.datetime.now().isoformat()


def datetime_next_day(datetime_obj):
    return datetime_obj + timedelta(days=1)

```

### 获得当天剩余时间

```
# -*- coding: utf-8 -*-
import datetime


def get_today_seconds_left():
    now = datetime.datetime.now()
    end = now.date() + datetime.timedelta(days=1)
    return int(time.mktime(end.timetuple()) - time.mktime(now.timetuple()))


def get_daily_left_seconds():
    now = datetime.datetime.now()
    last_second = datetime.datetime.combine(datetime.date.today(),
                                            datetime.time.max)
    return int((last_second - now).total_seconds())

```
