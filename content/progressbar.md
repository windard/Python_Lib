## progressbar

可以用来在终端里显示出像这种效果的进度条 `[==================             ] 25.60%` 的一个库。

当然我们也可以自己实现一个类似效果的进度条。

## 自行实现

```
# coding=utf-8

from __future__ import division
import math
import time
import sys

def progressbar(cur, total):
    percent = '{:.2%}'.format(cur / total)
    sys.stdout.write('\r')
    sys.stdout.write("[%-50s] %s" % (
                            '=' * int(math.floor(cur * 50 / total)),
                            percent))
    sys.stdout.flush()

t = 0
while t < 9.9:
	t += 0.1
	time.sleep(0.1)
	progressbar(t,10)
print

```

执行效果就是一个动态的增长的进度条的效果。

```
# python code\progressbar_demo.py
[================================================= ] 100.00%

```

或者像这个

```
# coding=utf-8

from __future__ import division

import sys,time
j = '#'
if __name__ == '__main__':
    for i in range(1,61):
        j += '#'
        sys.stdout.write(str(int((i/60)*100))+'%  ||'+j+'->'+"\r")
        sys.stdout.flush()
        time.sleep(0.5)
print
```

效果就是这样。

```
# python code\progressbar_demo2.py
100%  ||#############################################################->

```

还有这样，但是不能动态的显示已完成百分比。

```
# coding=utf-8

from __future__ import division

import sys,time
if __name__ == '__main__':
    for i in range(1,61):
        sys.stdout.write('#'+'->'+"\b\b")
        sys.stdout.flush()
        time.sleep(0.5)
print
```

效果是这样。

```
# spython code\progressbar_demo3.py
############################################################->

```

最后一个

```
# coding=utf-8

class progressbarClass:
  def __init__(self, finalcount, progresschar=None):
    import sys
    self.finalcount=finalcount
    self.blockcount=0
    #
    # See if caller passed me a character to use on the
    # progress bar (like "*"). If not use the block
    # character that makes it look like a real progress
    # bar.
    #
    if not progresschar: self.block=chr(178)
    else:        self.block=progresschar
    #
    # Get pointer to sys.stdout so I can use the write/flush
    # methods to display the progress bar.
    #
    self.f=sys.stdout
    #
    # If the final count is zero, don't start the progress gauge
    #
    if not self.finalcount : return
    self.f.write('\n------------------- % Progress -------------------\n')
    return

  def progress(self, count):
    #
    # Make sure I don't try to go off the end (e.g. >100%)
    #
    count=min(count, self.finalcount)
    #
    # If finalcount is zero, I'm done
    #
    if self.finalcount:
      percentcomplete=int(round(100*count/self.finalcount))
      if percentcomplete < 1: percentcomplete=1
    else:
      percentcomplete=100

    #print "percentcomplete=",percentcomplete
    blockcount=int(percentcomplete/2)
    #print "blockcount=",blockcount
    if blockcount > self.blockcount:
      for i in range(self.blockcount,blockcount):
        self.f.write(self.block)
        self.f.flush()

    if percentcomplete == 100: self.f.write("\n")
    self.blockcount=blockcount
    return

if __name__ == "__main__":
  from time import sleep
  # pb=progressbarClass(8,"*")
  pb=progressbarClass(8,"#")
  count=0
  while count < 9 :
    count+=1
    pb.progress(count)
    sleep(0.2)
```

结果就是这样

```
# python code\progressbar_demo4.py

------------------- % Progress -------------------
##################################################
```

但是这样的最好看

```
# -*- coding: utf-8 -*-
from __future__ import division
import sys
import time

def progress():
    for i in range(100):
        sys.stdout.write("\r[%s%s] %2d%%" % ('█' * i, ' ' * (99 - i), (i / 99) * 100))
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\n')


if __name__ == '__main__':
    progress()

```

效果是这样

```
# python download_progress_demo.py
[███████████████████████████████████████████████████████████████████████████████████████████████████] 100%
```

## progressbar

```
# coding=utf-8

from __future__ import division

import sys,time
import progressbar
total = 1000

# 基本用法
progress = progressbar.ProgressBar()
for i in progress(range(total)):
  time.sleep(0.01)

pbar = progressbar.ProgressBar().start()
for i in range(1,1000):
    pbar.update(int((i/(total-1))*100))
    time.sleep(0.01)
pbar.finish()

# 高级用法
widgets = ['Progress: ', progressbar.Percentage(), ' ', Bar(marker=progressbar.RotatingMarker('>-=')),
           ' ', progressbar.ETA(), ' ', progressbar.FileTransferSpeed()]
pbar = progressbar.ProgressBar(widgets=widgets, maxval=10000000).start()
for i in range(1000000):
  pbar.update(10*i+1)
  time.sleep(0.0001)
pbar.finish()

pbar = progressbar.ProgressBar(maxval=100,widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()]).start()
for i in xrange(100):
    time.sleep(0.01)
    pbar.update(i+1)

pbar.finish()
```

效果如下

```
$ python code\progressbar_first.py
100% |########################################################################|
100% |########################################################################|
Progress: 100% |>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>| Time: 0:00:02   3.82 MB/s
[========================================================================] 100%

```

还有一个官方给的例子

```
# coding=utf-8

import sys
import time
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer

examples = []
def example(fn):
    try: name = 'Example %d' % int(fn.__name__[7:])
    except: name = fn.__name__

    def wrapped():
        try:
            sys.stdout.write('Running: %s\n' % name)
            fn()
            sys.stdout.write('\n')
        except KeyboardInterrupt:
            sys.stdout.write('\nSkipping example.\n\n')

    examples.append(wrapped)
    return wrapped

@example
def example0():
    pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=300).start()
    for i in range(300):
        time.sleep(0.01)
        pbar.update(i+1)
    pbar.finish()

@example
def example1():
    widgets = ['Test: ', Percentage(), ' ', Bar(marker=RotatingMarker()),
               ' ', ETA(), ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets, maxval=10000000).start()
    for i in range(1000000):
        # do something
        pbar.update(10*i+1)
    pbar.finish()

@example
def example2():
    class CrazyFileTransferSpeed(FileTransferSpeed):
        """It's bigger between 45 and 80 percent."""
        def update(self, pbar):
            if 45 < pbar.percentage() < 80:
                return 'Bigger Now ' + FileTransferSpeed.update(self,pbar)
            else:
                return FileTransferSpeed.update(self,pbar)

    widgets = [CrazyFileTransferSpeed(),' <<<', Bar(), '>>> ',
               Percentage(),' ', ETA()]
    pbar = ProgressBar(widgets=widgets, maxval=10000000)
    # maybe do something
    pbar.start()
    for i in range(2000000):
        # do something
        pbar.update(5*i+1)
    pbar.finish()

@example
def example3():
    widgets = [Bar('>'), ' ', ETA(), ' ', ReverseBar('<')]
    pbar = ProgressBar(widgets=widgets, maxval=10000000).start()
    for i in range(1000000):
        # do something
        pbar.update(10*i+1)
    pbar.finish()

@example
def example4():
    widgets = ['Test: ', Percentage(), ' ',
               Bar(marker='0',left='[',right=']'),
               ' ', ETA(), ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets, maxval=500)
    pbar.start()
    for i in range(100,500+1,50):
        time.sleep(0.2)
        pbar.update(i)
    pbar.finish()

@example
def example5():
    pbar = ProgressBar(widgets=[SimpleProgress()], maxval=17).start()
    for i in range(17):
        time.sleep(0.2)
        pbar.update(i + 1)
    pbar.finish()

@example
def example6():
    pbar = ProgressBar().start()
    for i in range(100):
        time.sleep(0.01)
        pbar.update(i + 1)
    pbar.finish()

@example
def example7():
    pbar = ProgressBar()  # Progressbar can guess maxval automatically.
    for i in pbar(range(80)):
        time.sleep(0.01)

@example
def example8():
    pbar = ProgressBar(maxval=80)  # Progressbar can't guess maxval.
    for i in pbar((i for i in range(80))):
        time.sleep(0.01)

@example
def example9():
    pbar = ProgressBar(widgets=['Working: ', AnimatedMarker()])
    for i in pbar((i for i in range(50))):
        time.sleep(.08)

@example
def example10():
    widgets = ['Processed: ', Counter(), ' lines (', Timer(), ')']
    pbar = ProgressBar(widgets=widgets)
    for i in pbar((i for i in range(150))):
        time.sleep(0.1)

@example
def example11():
    widgets = [FormatLabel('Processed: %(value)d lines (in: %(elapsed)s)')]
    pbar = ProgressBar(widgets=widgets)
    for i in pbar((i for i in range(150))):
        time.sleep(0.1)

@example
def example12():
    widgets = ['Balloon: ', AnimatedMarker(markers='.oO@* ')]
    pbar = ProgressBar(widgets=widgets)
    for i in pbar((i for i in range(24))):
        time.sleep(0.3)

@example
def example13():
    # You may need python 3.x to see this correctly
    try:
        widgets = ['Arrows: ', AnimatedMarker(markers='←↖↑↗→↘↓↙')]
        pbar = ProgressBar(widgets=widgets)
        for i in pbar((i for i in range(24))):
            time.sleep(0.3)
    except UnicodeError: sys.stdout.write('Unicode error: skipping example')

@example
def example14():
    # You may need python 3.x to see this correctly
    try:
        widgets = ['Arrows: ', AnimatedMarker(markers='◢◣◤◥')]
        pbar = ProgressBar(widgets=widgets)
        for i in pbar((i for i in range(24))):
            time.sleep(0.3)
    except UnicodeError: sys.stdout.write('Unicode error: skipping example')

@example
def example15():
    # You may need python 3.x to see this correctly
    try:
        widgets = ['Wheels: ', AnimatedMarker(markers='◐◓◑◒')]
        pbar = ProgressBar(widgets=widgets)
        for i in pbar((i for i in range(24))):
            time.sleep(0.3)
    except UnicodeError: sys.stdout.write('Unicode error: skipping example')

@example
def example16():
    widgets = [FormatLabel('Bouncer: value %(value)d - '), BouncingBar()]
    pbar = ProgressBar(widgets=widgets)
    for i in pbar((i for i in range(180))):
        time.sleep(0.05)

@example
def example17():
    widgets = [FormatLabel('Animated Bouncer: value %(value)d - '),
               BouncingBar(marker=RotatingMarker())]

    pbar = ProgressBar(widgets=widgets)
    for i in pbar((i for i in range(180))):
        time.sleep(0.05)

@example
def example18():
    widgets = [Percentage(),
               ' ', Bar(),
               ' ', ETA(),
               ' ', AdaptiveETA()]
    pbar = ProgressBar(widgets=widgets, maxval=500)
    pbar.start()
    for i in range(500):
        time.sleep(0.01 + (i < 100) * 0.01 + (i > 400) * 0.9)
        pbar.update(i + 1)
    pbar.finish()

@example
def example19():
  pbar = ProgressBar()
  for i in pbar([]):
    pass
  pbar.finish()

try:
    for example in examples:
        example()
except KeyboardInterrupt:
    sys.stdout('\nQuitting examples.\n')


```

不知道为什么第十八个和十九个失败了。

## tqdm

tqdm 也可以实现一种比较好的实现命令行动态进度条的效果

```
# coding=utf-8

from time import sleep
from tqdm import tqdm

for i in tqdm(range(1, 500)):
    sleep(0.01)
```