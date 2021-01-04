# -*- encoding: utf-8 -*-
"""
@file: variable.py
@time: 2021/1/2 下午4:40
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""

# 问题: a，b的值是多少？
# def test1():
#     a = [1, 2, 3]
#     b = a
#     a[0], a[1], a[2] = 4, 5, 6
#     # a 和 b 的值都为 4， 5，6
#     print(a)
#     print(b)

import functools
from week07.test import test


def add(x, y):
    return x + y


def func(*args, **kwargs):
    # *args 以元祖的形式保存传入的参数
    # ** kwargs 以字典的形式保存传入的参数
    print(args)
    print(kwargs)


def line_conf(x, a):
    def line(b):
        return x * a + b

    return line


# 内部函数对外部函数作用域变量的引用
def counter(size=0):
    count = [0] * size

    def helper(index):
        count[index] += 1
        return count[index]

    return helper


# 使用nonlocal引用外部函数变量
def counter2(start):
    def helper():
        nonlocal start
        start += 1
        return start

    return helper


def main():
    pass

    # c1 = counter2(10)
    # # 输出 11，12
    # print(c1())
    # print(c1())

    # c1 = counter(2)
    # # 输出 1
    # print(c1(0))
    # # 输出 2
    # print(c1(0))
    # # 输出 1
    # print(c1(1))

    # line1 = line_conf(1, 2)
    # line2 = line_conf(3, 4)
    # # 输出：7， 17
    # print(line1(5), line2(5))
    #
    # # 输出：('b', ) . 内部函数变量名（编译函数保存的局部变量）
    # print(line1.__code__.co_varnames)
    # # 输出: ('a', 'x'). 外部函数变量名 (编译函数后的自由变量)
    # print(line1.__code__.co_freevars)
    # # 输出：2, 1. 传入外部函数值（自由变量的值）
    # print(line1.__closure__[0].cell_contents, line1.__closure__[1].cell_contents)

    # add_1 = functools.partial(add, 1)
    # # 输出：2
    # print(add_1(1))
    # # 输出：3
    # print(add_1(2))

    # func(1, 2, 3, name='jo')


if __name__ == '__main__':
    main()
