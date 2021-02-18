# -*- coding: utf-8 -*-

import funcy as fc
# only support in python2
from compiler.ast import flatten as ast_flatten


def flatten(elements):
    result = []
    for item in elements:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def old_flatten(elements):
    return [_ for item in elements for _ in old_flatten(item)] if isinstance(elements, list) else [elements]
    # result = []
    # for item in elements:
    #     if isinstance(item, list):
    #         item = old_flatten(item)
    #     else:
    #         item = [item]
    #     result.extend(item)
    # return result


if __name__ == '__main__':
    a = [1, 2, [3, 4, [5, 6], [7, 8]], [9, 10]]
    print(fc.flatten(a))
    print(ast_flatten(a))
    print(flatten(a))
