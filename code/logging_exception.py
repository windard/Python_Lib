# coding=utf-8

import sys
import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(lineno)-4d %(message)s', '%Y %b %d %a %H:%M:%S',)

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    logger.info("main start...")
    try:
        1 / 0
    except Exception as e:
        logger.exception("error %s", e)
    logger.info("main end.")
