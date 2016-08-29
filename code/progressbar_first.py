# coding=utf-8

from __future__ import division
 
import sys,time
import progressbar
total = 1000
 
#基本用法
progress = progressbar.ProgressBar()
for i in progress(range(total)):
  time.sleep(0.01)
 
pbar = progressbar.ProgressBar().start()
for i in range(1,1000):
    pbar.update(int((i/(total-1))*100))
    time.sleep(0.01)
pbar.finish()
 
#高级用法
widgets = ['Progress: ', progressbar.Percentage(), ' ', progressbar.Bar(marker=progressbar.RotatingMarker('>-=')),
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