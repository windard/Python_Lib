## asyncore

基本的异步 io 处理模块，网络中一次处理多个连接的的三种解决方案：多线程，多进程，或者 异步 IO。

多进程的系统开销比较大，多线程难以管理，异步 IO 正在越来越受到欢迎，像 nodejs 就大量使用异步 IO 操作，降低系统开销而且能够获得不错的效果，web 服务器 Nginx 也支持各种 异步 IO 的类型，如 select，poll ，epoll 等。

可惜 windows  下只能使用 select 。


