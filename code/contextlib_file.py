# coding=utf-8

from contextlib import contextmanager


@contextmanager
def open_file(name, mode='r'):
    f = open(name, mode)
    yield f
    f.close()

with open_file("./contextlib_file.py") as f:
    for i in f:
        print i,

with open_file("/tmp/a", "a") as f:
    f.write("hello world ~ ")
