# utf-8

import sys
import logging

logger = logging.getLogger("Xidian Spider")
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)-3d] %(levelname)-8s %(lineno)-4d %(message)s', '%Y %b %d, %a %H:%M:%S')

file_handler = logging.FileHandler("XidianSpider.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)

logger.setLevel(logging.DEBUG)


