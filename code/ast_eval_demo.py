# -*- coding: utf-8 -*-

import ast


if __name__ == '__main__':
    # 赋值操作不能有
    # print ast.literal_eval("a=1")
    # print eval("a=1")
    # a = 1
    # 加减乘除都不能有
    # print ast.literal_eval("1+1")
    # print eval("1+1")
    # print ast.literal_eval("1==1")
    print eval("1==1")
    print ast.literal_eval("1")
    print ast.literal_eval("None")
    # 连集合都不能有
    # print ast.literal_eval("{1,2,4}")
    # print ast.literal_eval("set([1])")
    # print ast.literal_eval("[1,2,{'1', 2, '2,3,4'}, [4,5,'6']]")
    # print [1,2,{'1', 2, '2,3,4'}, [4,5,'6']]
    print ast.literal_eval("[1,2,3,{2:3}]")
    # 连最终结果是一个list也不行
    # print ast.literal_eval("list([1,2,3])")
    print list([1, 2, 3])
    # print ast.literal_eval("[1,2+3]")
    # 复数可以有，负数也可以有
    print ast.literal_eval("1+2j")
    print ast.literal_eval("-2")
    # print ast.literal_eval("--2")
    # 正数就不行
    # print ast.literal_eval("+2")
    # print ast.literal_eval("++2")
