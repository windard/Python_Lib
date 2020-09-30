# coding=utf-8

import time
import random
from tqdm import tqdm


count = 0
total = 1024
progress = tqdm(total=total, unit='B',unit_scale=True, desc='filename')


while count < total:
	time.sleep(1)
	step = random.randrange(100)
	count += step
	progress.update(step)

progress.close()
