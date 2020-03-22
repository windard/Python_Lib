# coding=utf-8

import inspect


def get_frame():
    """
    帧是当前的上下文，调用时的环境变量和数据
    """
    frame = inspect.currentframe()
    print 'line {} of {}'.format(frame.f_lineno, frame.f_code.co_filename)
    print 'locals: {}'.format(frame.f_locals)


def get_stack():
    """
    栈是用来展示调用链路，每一层都是一个帧
    """
    for frame, filename, lineno, func, code_context, code_index in inspect.stack():
        print('{}[{}]\n -> {}:{}'.format(
            filename,
            lineno,
            func,
            code_context[code_index].strip()
        ))
        print frame.f_locals


if __name__ == '__main__':
    frame = inspect.currentframe()
    print 'line {} of {}'.format(frame.f_lineno, frame.f_code.co_filename)
    print 'locals: {}'.format(frame.f_locals)

    get_frame()
    get_stack()
