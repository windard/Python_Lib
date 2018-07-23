# -*- coding: utf-8 -*-

import signal
import requests


def timeoutFn(func, args=(), kwargs={}, timeout_duration=5, default=None):

    class TimeoutError(Exception):
        pass

    def handler(signum, frame):
        raise TimeoutError()

    # set the timeout handler
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout_duration)
    try:
        result = func(*args, **kwargs)
    except TimeoutError as exc:
        result = default
    finally:

        signal.alarm(0)
        signal.signal(signal.SIGALRM, signal.SIG_DFL)
    return result


if __name__ == '__main__':
    print timeoutFn(requests.get, ("https://baidu.com", ), default='failed')
    print timeoutFn(requests.get, ("https://google.com", ), default='failed')
