# coding=utf-8

import time
from datetime import datetime

# # timestamp
# print time.time()
# print int(time.time())

# # ISO 8601
# print time.strftime('%F %T%z (%Z)')
# print time.strftime('%Y-%m-%d %H:%M:%S')

# # RFC-2822
# print time.strftime('%c')
# print time.asctime()
# print time.ctime()

# time.struct_time
# print time.localtime()


# ISO 8601
print datetime.now()
print datetime.utcnow()
