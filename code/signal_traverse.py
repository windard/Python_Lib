# -*- coding: utf-8 -*-

import signal


def alarm_received(n, stack):
    return


signal.signal(signal.SIGALRM, alarm_received)


# SIG_ING 如果信号被忽略
# SIG_DFL 如果使用默认行为
# SIG_IGN -- if the signal is being ignored
# SIG_DFL -- if the default action for the signal is in effect
# None -- if an unknown handler is in effect
# anything else -- the callable Python object used as a handler
signals_to_names = dict(
    (getattr(signal, n), n)
    for n in dir(signal)
    if n.startswith('SIG') and '_' not in n
)

for s, name in sorted(signals_to_names.items()):
    handler = signal.getsignal(s)
    if handler is signal.SIG_DFL:
        handler = 'SIG_DFL'
    elif handler is signal.SIG_IGN:
        handler = 'SIG_IGN'
    print '%-10s (%2d):' % (name, s), handler
