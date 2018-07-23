# -*- coding: utf-8 -*-

import time
import signal


# After finish alarm
def receive_alarm(signum, stack):
    print 'Alarm :', time.ctime()


# Call receive_alarm with 2 seconds
signal.signal(signal.SIGALRM, receive_alarm)
print 'Before:', time.ctime()

# Unix only
signal.alarm(2)
print 'After alarm :', time.ctime()

# Alarm will finish sleep
time.sleep(3)
print 'After sleep :', time.ctime()
