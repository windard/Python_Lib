# -*- coding: utf-8 -*-
import time
import funcy as fc

from functools import wraps
from compiler.ast import flatten as ast_flatten


def flatten(elements):
    return [_ for item in elements for _ in flatten(item)] if isinstance(elements, list) else [elements]


@fc.once
def call_once():
    print("only once called")


@fc.once
def call_once_with_args(x):
    print("only once with args called")


if __name__ == '__main__':
    a = [1, 2, [3, 4, [5, 6], [7, 8]], [9, 10]]
    print(fc.flatten(a))
    print(ast_flatten(a))
    print(flatten(a))

    call_once()
    call_once()
    call_once_with_args(1)
    call_once_with_args(2)
