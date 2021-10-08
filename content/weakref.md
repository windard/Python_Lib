## weakref

正常的引用会将引用计数器加一，最后在引用计数为零的时候删除，回收内存。

使用弱引用类型不会将计数器加一，可以减少避免循环引用，长期占有内存的情况。

可以使用 `sys.getrefcount` 来查看一个对象的引用次数。