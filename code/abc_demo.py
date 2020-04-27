# coding=utf-8
import abc


class A(object):
    __metaclass__ = abc.ABCMeta


class B(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def parse(self):
        return B

    @abc.abstractproperty
    def name(self):
        return "B"


class BB(B):
    def parse(self):
        return super(BB, self).parse()

    @property
    def name(self):
        return super(BB, self).name


A.register(tuple)


if __name__ == '__main__':
    a = A()
    # b = B()
    # print(b.parse())
    bb = BB()
    print(bb.parse())
    print(bb.name)

    print issubclass(tuple, A)
    print isinstance((), A)
