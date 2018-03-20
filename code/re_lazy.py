# coding=utf-8

import re

m = re.match(r'<html>(.*)', "<html><body><title>this is title</title></body></html>>")

print m.group()

m = re.match(r'<html>(.*?)', "<html><body><title>this is title</title></body></html>>")

print m.group()
