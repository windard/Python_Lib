## abc

abc = Abstract Base Class 抽象基类

### ABCMeta

使用 ABCMeta 元类定义一个抽象基类。

当定义一个类的 metaclass 为抽象基类时，`既可以被继承，也可以创建实例`，与 Java 中的抽象类或者接口完全不一样。

在 python 2 中使用 `__metaclass__ = abc.ABCMeta` 来声明元类

在 python 3 中使用 `class A(object, metaclass = Meta):` 来声明元类

可以使用 `@six.add_metaclass(Meta)` 装饰器来修饰，兼容 2 和 3

```
# coding=utf-8
import abc


class A(object):
    __metaclass__ = abc.ABCMeta


if __name__ == '__main__':
    a = A()

```

那 ABCMeta 的主要功能是什么呢？强行认爹，比如将 A 认为是 tuple 的父类。

```
# coding=utf-8
import abc


class A(object):
    __metaclass__ = abc.ABCMeta


A.register(tuple)


if __name__ == '__main__':

    print issubclass(tuple, A)
    print isinstance((), A)

```

### 抽象方法和抽象属性

python 中的静态方法和类方法都是关键字，`classmethod` 和 `staticmethod` ，但是抽象方法不是，它只是在 abc 这个模块中的一个装饰器，放在一个类的方法上作为抽象方法，在子类中实现。

为什么使用 `ABCMeta` 定义抽象类之后还能进行生成实例呢？因为抽象类没有抽象方法，如果有抽象方法，那么这个类就不能被实例化。

抽象类和抽象方法必须结合起来使用
- 只有抽象类，没有抽象方法，可以进行实例化
- 只有抽象方法，没有抽象类，可以进行实例化

如果继承抽象类，没有实现抽象方法，那也不能实例化。

```
# coding=utf-8
import abc


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


if __name__ == '__main__':
    # b = B()
    # print(b.parse())
    bb = BB()
    print(bb.parse())
    print(bb.name)

```

### 参考资料

[abc](https://docs.python.org/zh-cn/2.7/library/abc.html)
