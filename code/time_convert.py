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
    """将字符串格式的时间 (含毫秒) 转为 datetiem 格式
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