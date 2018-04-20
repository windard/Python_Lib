# -*- coding: utf-8 -*-

import multiprocessing


def decrease(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = - a[i]


if __name__ == '__main__':
    num = multiprocessing.Value('d', 0.0)
    arr = multiprocessing.Array('i', range(10))

    p = multiprocessing.Process(target=decrease, args=(num, arr))
    p.start()
    p.join()

    print(num.value)
    print(arr[:])
