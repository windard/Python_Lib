#coding=utf-8
import re

pattern = re.compile(r"he")

match = pattern.match("hello , world")

if match:
    print match.group()

