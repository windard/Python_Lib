# coding=utf-8

import time
from tqdm import trange, tqdm

for i in trange(10):
    time.sleep(0.1)

for i in tqdm(range(100)):
    time.sleep(0.1)
