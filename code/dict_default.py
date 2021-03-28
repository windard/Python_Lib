# -*- coding: utf-8 -*-

from collections import defaultdict, Counter


if __name__ == '__main__':
    default_list = defaultdict(list)
    default_list["a"].append(1)
    default_list["a"].append(2)
    default_list["a"].append(3)
    print(default_list)

    default_zero = Counter()
    default_zero["b"] += 1
    default_zero["b"] += 2
    default_zero["b"] += 3
    print(default_zero)
