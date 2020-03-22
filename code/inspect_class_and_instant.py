# coding=utf-8

import inspect
import example


def detect_class():
    print("A:")
    for name, data in inspect.getmembers(example.A):
        print('{} : {}'.format(name, data))


def detect_method():
    print("A:")
    for name, data in inspect.getmembers(example.A, inspect.ismethod):
        print('{} : {}'.format(name, data))
    print("B:")
    for name, data in inspect.getmembers(example.B, inspect.ismethod):
        print('{} : {}'.format(name, data))
    print("a:")
    for name, data in inspect.getmembers(example.a, inspect.ismethod):
        print('{} : {}'.format(name, data))


if __name__ == '__main__':
    detect_class()
    detect_method()
