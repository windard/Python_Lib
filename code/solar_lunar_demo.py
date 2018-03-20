# coding=utf-8

import datetime
from LunarSolarConverter.LunarSolarConverter import (
    Solar,
    LunarSolarConverter,
)

def get_today():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day

    converter = LunarSolarConverter()
    solar = Solar(year, month, day)
    lunar = converter.SolarToLunar(solar)

    solar_today = '{}-{}-{}'.format(solar.solarYear,
                                    solar.solarMonth,
                                    solar.solarDay)
    lunar_today = '{}-{}-{}'.format(lunar.lunarYear,
                                    lunar.lunarMonth,
                                    lunar.lunarDay)
    return solar_today, lunar_today


def main():
    print get_today()


if __name__ == '__main__':
    main()
