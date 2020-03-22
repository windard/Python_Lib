# coding=utf-8

import inspect

import example


def detect_all():
    for name, data in inspect.getmembers(example):
        if name.startswith('__'):
            continue
        print('{} : {}'.format(name, data))


def detect_class():
    for name, data in inspect.getmembers(example, inspect.isclass):
        if name.startswith('__'):
            continue
        print('{} : {}'.format(name, data))


def detect_code():
    for name, data in inspect.getmembers(example, inspect.iscode):
        if name.startswith('__'):
            continue
        print('{} : {}'.format(name, data))


def detect_function():
    for name, data in inspect.getmembers(example, inspect.isfunction):
        if name.startswith('__'):
            continue
        print('{} : {}'.format(name, data))


if __name__ == '__main__':
    print "all:"
    detect_all()
    print "class:"
    detect_class()
    print "function:"
    detect_function()
    print "code:"
    detect_code()
