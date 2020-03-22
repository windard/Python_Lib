# coding=utf-8

import inspect
import example

if __name__ == '__main__':

    print inspect.getcomments(example)
    print inspect.getdoc(example)
    print inspect.getdoc(example.A)
    print inspect.getdoc(example.B.hello)

    print inspect.findsource(example.A)

    print inspect.getabsfile(example.A)
    print inspect.getfile(example.A)
    print inspect.getsource(example)
    print inspect.getsource(example.A)
    print inspect.getsourcefile(example.A)
    print inspect.getsourcelines(example.A)

    print inspect.getmodule(example.A)
    print inspect.getmoduleinfo("example.py")
    print inspect.getmodulename("example.py")
