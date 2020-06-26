# -*- coding: utf-8 -*-

import os
import time
import logging
import signal

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(name)-25s %(asctime)s %(levelname)-8s %(lineno)-4d %(message)s',
    datefmt='[%Y %b %d %a %H:%M:%S]',
)


def receive_signal(signum, stack):
    logger.info('Received: %s', signum)


if __name__ == '__main__':

    # Register signal handlers
    signal.signal(signal.SIGHUP, receive_signal)
    signal.signal(signal.SIGINT, receive_signal)
    signal.signal(signal.SIGQUIT, receive_signal)
    # signal.signal(signal.SIGKILL, receive_signal)
    # signal.signal(signal.SIGSTOP, receive_signal)

    signal.signal(signal.SIGTERM, receive_signal)
    signal.signal(signal.SIGTSTP, receive_signal)
    signal.signal(signal.SIGCONT, receive_signal)

    signal.signal(signal.SIGUSR1, receive_signal)
    signal.signal(signal.SIGUSR2, receive_signal)

    # Print the process ID so it can be used with 'kill'
    # to send this program signals.
    logger.info('My PID is: %s', os.getpid())

    for i in range(20):
        logger.info('Waiting...')
        time.sleep(30)
