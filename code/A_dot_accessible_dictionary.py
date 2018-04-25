# -*- coding: utf-8 -*-


class DotDict(dict):

    def __init__(self):
        super(DotDict, self).__init__()
        self.__dict__ = self


if __name__ == '__main__':

    a = DotDict()
    a['name'] = 'windard'
    a.year = 24
    print a
