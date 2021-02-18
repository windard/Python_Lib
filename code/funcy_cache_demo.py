# -*- coding: utf-8 -*-
import time
import funcy as fc

from functools import wraps


def cache(func):
    local_cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = "{}:{}".format(";".join(map(str, args)),
                             ";".join(["{}:{}".format(*map(str, item)) for item in sorted(kwargs.items())]))
        if key in local_cache:
            return local_cache[key]
        else:
            value = func(*args, **kwargs)
            local_cache[key] = value
            return value

    return wrapper


# @cache
@fc.memoize
def get_timestamp(x):
    return int(time.time())


if __name__ == '__main__':
    print(get_timestamp(1))
    time.sleep(1)
    print(get_timestamp(1))
    time.sleep(1)
    print(get_timestamp(1))
    time.sleep(2)
    print(get_timestamp(2))
    time.sleep(1)
    print(get_timestamp(2))
    print(get_timestamp.memory)