# coding=utf-8

import inspect
import example


def main(a=1):
    print inspect.getargvalues(inspect.currentframe())


if __name__ == '__main__':
    main()
    print inspect.getargspec(example.add)
    print inspect.formatargspec(inspect.getargspec(example.add))
    print inspect.getargspec(example.B.hello)
    print inspect.getcallargs(example.add, 1, 2)
    print inspect.getcallargs(example.B.hello, self=None, word="world")
