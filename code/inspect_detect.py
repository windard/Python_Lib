# coding=utf-8

import inspect
import example

if __name__ == '__main__':
    print inspect.isbuiltin(apply)
    print inspect.isbuiltin(lambda: None)
    print inspect.isclass(type)
    print inspect.isclass(1)
    print inspect.iscode(example.add.func_code)
    print inspect.iscode(example.B.hello.im_func.func_code)
    print inspect.iscode("1+1")
    print inspect.ismodule(inspect)
    print inspect.isfunction(input)
    print inspect.isgenerator(iter([]))
    print inspect.isgenerator([])
