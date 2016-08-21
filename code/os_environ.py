# coding=utf-8

import os

environment = os.environ

for i,j in environment.items():
	print "%s : %s "%(i,j)