## geohash

geohash 是经纬度的一种表示方式，将经纬度转换为字符串。

geohash，5位代表5公里，6位代表1公里，7位只有几百米,  8位的geohash 编码的经度能达到19米左右，9位的geohash经度能达到米级


|length  |      lat bits |    lng bits   |lat error|   lng error   |  km error        |
|-------|--------------|----------------|--------|--------------|--------------------|
|1   |         2     |        3          | ±23         | ±23           | ±2500       |
|2   |         5     |        5          | ±2.8.       | ±5.6.         | ±630        |
|3   |         7     |        8          | ±0.70       | ±0.70         | ±78     |
|4   |         10     |        10         | ±0.087      | ±0.18.        | ±20        |
|5   |         12     |        13         | ±0.022      | ±0.022        | ±2.4       |
|6   |         15     |        15         | ±0.0027     | ±0.0055       | ±0.61      |
|7   |         17     |      18         | ±0.00068    | ±0.00068      | ±0.076       |
|8   |         20     |        20         | ±0.00008    | ±0.00017      | ±0.019     |
|9   |           22     |        23         | ±0.00002    | ±0.000021     | ±0.00478     |
|10   |       25     |        25         | ±0.000002.  | ±0.0000054.   | ±0.0006     |
|11   |       27     |        28         | ±0.00000067 | ±0.00000067.  | ±0.00015        |

使用

- geohash.encode 编码
- geohash.decode 解码

实际的 geohash 编码非常简单，很容易自己实现

```
# -*- coding: utf-8 -*-

import string
import geohash


base32_string = (string.digits + string.lowercase) \
    .replace('a', '').replace('i', '').replace('o', '').replace('l', '')


def convert_to_binary(latitude, longitude, length=25):
    bin_longitude = ''
    bin_latitude = ''
    static_longitude = [-180.0, 180.0]
    static_latitude = [-90.0, 90.0]
    for i in range(length):
        middle_longitude = sum(static_longitude) / 2
        if longitude < middle_longitude:
            bin_longitude += '0'
            static_longitude = [static_longitude[0], middle_longitude]
        else:
            bin_longitude += '1'
            static_longitude = [middle_longitude, static_longitude[1]]

        middle_latitude = sum(static_latitude) / 2
        if latitude < middle_latitude:
            bin_latitude += '0'
            static_latitude = [static_latitude[0], middle_latitude]
        else:
            bin_latitude += '1'
            static_latitude = [middle_latitude, static_latitude[1]]

    return bin_latitude, bin_longitude


def base32_encode(bin_latitude, bin_longitude):

    bin_geo = ''

    for i in range(len(bin_longitude)):
        bin_geo += bin_longitude[i]
        bin_geo += bin_latitude[i]

    geo_hash = ''

    for i in range(0, len(bin_geo), 5):
        geo_hash += base32_string[int(bin_geo[i:i+5], 2)]

    return geo_hash


def base32_decode(geo_hash):
    bin_string = "".join(["{:05b}".format(base32_string.index(i))
                          for i in geo_hash])

    bin_longitude = "".join([bin_string[i]
                             for i in range(0, len(bin_string), 2)])
    bin_latitude = "".join([bin_string[i]
                            for i in range(1, len(bin_string), 2)])

    return bin_latitude, bin_longitude


def convert_from_binary(bin_latitude, bin_longitude):
    static_longitude = [-180.0, 180.0]
    static_latitude = [-90.0, 90.0]
    for i in bin_longitude:
        middle_longitude = sum(static_longitude) / 2
        if i == '0':
            static_longitude = [static_longitude[0], middle_longitude]
        else:
            static_longitude = [middle_longitude, static_longitude[1]]

    middle_longitude = sum(static_longitude) / 2

    for i in bin_latitude:
        middle_latitude = sum(static_latitude) / 2
        if i == '0':
            static_latitude = [static_latitude[0], middle_latitude]
        else:
            static_latitude = [middle_latitude, static_latitude[1]]

    middle_latitude = sum(static_latitude) / 2
    return middle_latitude, middle_longitude


def geo_encode(latitude, longitude, length=25):
    return base32_encode(*convert_to_binary(latitude, longitude, length))


def geo_decode(geo_hash):
    return convert_from_binary(*base32_decode(geo_hash))


if __name__ == '__main__':
    longitude = 110.082600
    latitude = 34.477861

    length = 30
    print latitude, longitude
    bin_lat, bin_lon = convert_to_binary(latitude, longitude, length)
    print bin_lat, bin_lon
    print base32_encode(bin_lat, bin_lon)
    print base32_decode(base32_encode(bin_lat, bin_lon))
    print convert_from_binary(*base32_decode(base32_encode(bin_lat, bin_lon)))

    print geohash.encode(36.255833, 117.103367)
    print geo_encode(36.255833, 117.103367)
    print geohash.encode(36.255833, 117.103367)
    print geo_encode(36.255833, 117.103367)
    print geohash.encode(36.255833, 117.103367)
    print geo_encode(36.255833, 117.103367)

    print geohash.decode('wx0csn0ng8')
    print geo_decode('wx0csn0ng8')
    print geohash.decode('ww0k7k0et7')
    print geo_decode('ww0k7k0et7')

```