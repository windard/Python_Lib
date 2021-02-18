# -*- coding: utf-8 -*-
import time
import funcy as fc

from functools import wraps

# def retry(times=3):
#     def inner(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             for i in range(times):
#                 try:
#                     return func(*args, **kwargs)
#                 except Exception as e:
#                     if i == times-1:
#                         raise e
#                     print("occur error:%r" % e)
#
#         return wrapper
#     return inner

# def retry(times=3):
#     def inner(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             try:
#                 return func(*args, **kwargs)
#             except Exception as e:
#                 if times <= 1:
#                     raise e
#                 print("occur error:%r" % e)
#                 return retry(times-1)(func)(*args, **kwargs)
#
#         return wrapper
#
#     return inner


def retry(times=3):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            count = 0
            while count < times:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print("occur error:%r" % e)
                    count += 1
            raise
        return wrapper

    return inner


@fc.retry(5)
# @retry(3)
def raise_exception():
    time.sleep(1)
    return 1 / 0


if __name__ == '__main__':
    print(raise_exception())
