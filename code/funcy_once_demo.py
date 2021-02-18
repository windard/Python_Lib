# -*- coding: utf-8 -*-
import funcy as fc


@fc.once
def call_once():
    print("only once called")


@fc.once
def call_once_with_args(x):
    print("only once with args called")


if __name__ == '__main__':
    call_once()
    call_once()
    call_once_with_args(1)
    call_once_with_args(2)
