## datetime

datetime 和 timestamp(int) 的相互转换，在时间处理的时候，见到的最多的时间表示方式就是这两者了，时间的表示格式既可以使用 timestamp ，也可以选择使用 datetime 或者是 struct_time ，但是在数据库中一般常见的是是用 integer 或者 datetime 这两种类型存储，那么这三者的转换关系呢？

> datatime 之间混乱的关系终于有人能出来解决一下，requests 作者 Kennethreitz 的 [Maya: Datetimes for Humans™](https://github.com/kennethreitz/maya) 可以看一看

### 时间的几种表现形式

UTC (Coordinated Universal Time) 是一种时间标准，以 1970年1月1日0时0分0秒的格林尼治时间为起点的时间计量标准，这一时间点也被称为 普朗克时间 (epoch time)。该标准将全世界分为 24 个时区，中国位于 UTC+8 的时区之内。现在全世界的计算机时间也都是采用这一标准。

常见的时区 `GMT(Greenwich Mean Time)` 格林尼治时间， `CST(China Standard Time)` 中国标准时间。

#### ISO 8601

ISO 8601的标准格式是：`YYYY-MM-DDTHH:mm:ss.sssZ`

- `YYYY`：年份，0000 ~ 9999
- `MM`：月份，01 ~ 12
- `DD`：日，01 ~ 31
- `T`：分隔日期和时间，可以使用 `T` 或者空格。
- `HH`：小时，00 ~ 24
- `hh`: 小时，0-12
- `mm`：分钟，00 ~ 59
- `ss`：秒，00 ~ 59
- `.sss`：毫秒
- `Z`：时区，可以是：Z(格林尼治时间)、+HH:mm、-HH:mm

> `T` 只是日期和时间的间隔符  
> `Z` 表示标准时间 `UTC`

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

python中时间日期格式化符号：

- `%y` 两位数的年份表示（00-99）
- `%Y` 四位数的年份表示（000-9999）
- `%m` 月份（01-12）
- `%d` 月内中的一天（0-31）
- `%H` 24小时制小时数（0-23）
- `%I` 12小时制小时数（01-12）
- `%M` 分钟数（00=59）
- `%S` 秒（00-59）
- `%a` 本地简化星期名称
- `%A` 本地完整星期名称
- `%b` 本地简化的月份名称
- `%B` 本地完整的月份名称
- `%c` 本地相应的日期表示和时间表示
- `%j` 年内的一天（001-366）
- `%p` 本地A.M.或P.M.的等价符
- `%U` 一年中的星期数（00-53）星期天为星期的开始
- `%w` 星期（0-6），星期天为星期的开始
- `%W` 一年中的星期数（00-53）星期一为星期的开始
- `%x` 本地相应的日期表示
- `%X` 本地相应的时间表示
- `%Z` 当前时区的名称
- `%%` %号本身

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

#### 原生时间

在正常使用 `datetime` 库的时候，默认使用的是带时区偏移的原生时间，或者叫 `naive`。

如何查看,对比 `datetime.datetime.now()` 和 `datetime.datetime.utcnow()` 是否一致就知道了。

datetime 是有时区的，时间戳是没有时区的。所以查看 `datetime.datetime.fromtimestamp(0)` 和 `datetime.datetime.utcfromtimestamp(0)` 是否一致也可以判断。

```
In [119]: datetime.datetime.now()
Out[119]: datetime.datetime(2020, 10, 21, 14, 18, 32, 502615)

In [120]: datetime.datetime.utcnow()
Out[120]: datetime.datetime(2020, 10, 21, 6, 18, 36, 778644)

In [121]: datetime.datetime.fromtimestamp(0)
Out[121]: datetime.datetime(1970, 1, 1, 8, 0)

In [122]: datetime.datetime.utcfromtimestamp(0)
Out[122]: datetime.datetime(1970, 1, 1, 0, 0)
```

#### 时区时间

正常使用 datetime 一点问题没有，但是如果想要做时区转换的时候，就会有问题，因为没有指定时区，也就不能转换时区。

一般常见的时区库有 `pytz` 和 `dateutil.tz`

本人当前在上海，也就是东八区，是格林尼治时间加八个小时，时区一般表示为 `Asia/Shanghai`

所以可以使用精确的时区时间，就是指定时区的原生时间，或者叫 `aware`。

```
In [130]: from dateutil import tz

In [131]: datetime.datetime.now()
Out[131]: datetime.datetime(2020, 10, 21, 14, 25, 52, 296661)

In [132]: datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
Out[132]: datetime.datetime(2020, 10, 21, 14, 26, 23, 897680, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>)

In [133]: datetime.datetime.now().tzname()

In [134]: datetime.datetime.now().tzinfo

In [135]: datetime.datetime.now(pytz.timezone('Asia/Shanghai')).tzinfo
Out[135]: <DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>

In [136]: datetime.datetime.now(pytz.timezone('Asia/Shanghai')).tzname()
Out[136]: 'CST'

In [137]: datetime.datetime.now(tz.tzlocal())
Out[137]: datetime.datetime(2020, 10, 21, 14, 27, 35, 106503, tzinfo=tzlocal())

In [138]: datetime.datetime.now(tz.tzlocal()).tzname()
Out[138]: 'CST'

In [139]: datetime.datetime.now(tz.tzlocal()).tzinfo
Out[139]: tzlocal()
```

转换时区的时候即可以使用 datetime.datetime 的 `astimezone` 函数即可修改时区, 如果是原生时间则无法转化时区

```

In [140]: t = datetime.datetime.now(tz.tzlocal())

In [141]: t.astimezone(pytz.timezone('Asia/Shanghai'))
Out[141]: datetime.datetime(2020, 10, 21, 14, 28, 12, 598259, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>)

In [142]: t.astimezone(pytz.timezone('UTC'))
Out[142]: datetime.datetime(2020, 10, 21, 6, 28, 12, 598259, tzinfo=<UTC>)

In [143]: t.astimezone(tzutc())
Out[143]: datetime.datetime(2020, 10, 21, 6, 28, 12, 598259, tzinfo=tzutc())
```

所以，一些 utc 的操作也可以转化一下

```
In [144]: datetime.datetime.now()
Out[144]: datetime.datetime(2020, 10, 21, 14, 31, 0, 66343)

In [145]: datetime.datetime.utcnow()
Out[145]: datetime.datetime(2020, 10, 21, 6, 31, 2, 295432)

In [149]: datetime.datetime.now(tz.tzutc())
Out[149]: datetime.datetime(2020, 10, 21, 6, 32, 54, 761768, tzinfo=tzutc())

In [150]: datetime.datetime.now(pytz.utc)
Out[150]: datetime.datetime(2020, 10, 21, 6, 33, 42, 768778, tzinfo=<UTC>)

In [168]: datetime.datetime.fromtimestamp(0)
Out[168]: datetime.datetime(1970, 1, 1, 8, 0)

In [170]: datetime.datetime.fromtimestamp(0, tz=tz.tzutc())
Out[170]: datetime.datetime(1970, 1, 1, 0, 0, tzinfo=tzutc())

In [171]: datetime.datetime.fromtimestamp(0, tz=pytz.timezone('UTC'))
Out[171]: datetime.datetime(1970, 1, 1, 0, 0, tzinfo=<UTC>)

In [173]: datetime.datetime.utcfromtimestamp(0)
Out[173]: datetime.datetime(1970, 1, 1, 0, 0)
```

#### 时区转化

如果你已经有一个原生时间，现在想做时区转化，比如你在北京时间下午三点，你想看下你在洛杉矶的朋友现在几点。

那么首先需要将原生时间转化为时区时间，然后再做时区转化。

```
In [3]: d = datetime.datetime.now()

In [4]: timezone = pytz.timezone('Asia/Shanghai')

In [5]: d_aware = timezone.localize(d)

In [6]: d
Out[6]: datetime.datetime(2020, 10, 21, 15, 37, 23, 397858)

In [7]: d_aware
Out[7]: datetime.datetime(2020, 10, 21, 15, 37, 23, 397858, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>)

In [8]: d_aware.astimezone(pytz.timezone("America/Los_Angeles"))
Out[8]: datetime.datetime(2020, 10, 21, 0, 37, 23, 397858, tzinfo=<DstTzInfo 'America/Los_Angeles' PDT-1 day, 17:00:00 DST>)

In [9]: d_aware.astimezone(pytz.utc)
Out[9]: datetime.datetime(2020, 10, 21, 7, 37, 23, 397858, tzinfo=<UTC>)
```

那你的洛杉矶朋友应该是今天早上零点，或者说昨天晚上十二点。

#### 所有时区

获取时区

```
In [174]: pytz.timezone('Asia/Shanghai')
Out[174]: <DstTzInfo 'Asia/Shanghai' LMT+8:06:00 STD>

In [175]:

In [175]: pytz.country_timezones('cn')
Out[175]: [u'Asia/Shanghai', u'Asia/Urumqi']
```

使用 `pytz.country_names` 查看所有的支持的国家和地区简写

使用 `pytz.all_timezones` 或者 `common_timezones` 查看所有支持的时区

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


### 获取今天的第一秒和最后一秒

```
first_second = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
last_second = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
```

