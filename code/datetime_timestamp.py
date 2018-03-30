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
