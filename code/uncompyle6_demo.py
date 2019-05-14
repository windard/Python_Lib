# coding=utf-8

import uncompyle6

with open("test.py", "w") as f:
    print uncompyle6.uncompyle_file("test.pyc", f)
