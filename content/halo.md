## halo

halo 是一个在终端的旋转等待的小光圈

```
# -*- coding: utf-8 -*-

import time
from halo import Halo

spinner = Halo(text='Loading', spinner='dots')
spinner.start()

# Run time consuming work here
# You can also change properties for spinner as and when you want
time.sleep(5)

spinner.stop()

```

或者高级一点的用法

```
# -*- coding: utf-8 -*-

import time

from halo import Halo

@Halo(text=u'下载中', color='yellow', spinner={
    'interval': 100,
    'frames': ['-', '+', '*', '+', '-']
}, animation='marquee')
def loading():
    time.sleep(4)


def sun():
    time.sleep(5)


if __name__ == '__main__':
    loading()
    with Halo(text='Sun', spinner='moon'):
        sun()

```

