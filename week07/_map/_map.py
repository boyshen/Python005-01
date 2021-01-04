# -*- encoding: utf-8 -*-
"""
@file: _map.py
@time: 2021/1/4 上午11:52
@author: shenpinggang
@contact: 1285456152@qq.com
@desc:  实现 map() 函数的功能。
"""


def square(x):
    """
    自定义函数
    :param x: (int)
    :return: (int)
    """
    return x * x


class Map_(object):
    """
    自实现 map 操作
    """

    def __init__(self, func, iterables):
        self.func = func
        self.iterables = iterables
        self.idx = 0
        self.size = len(self.iterables)

    @classmethod
    def map(cls, func, iterables):
        return cls(func, iterables)

    def __iter__(self):
        return self

    def __next__(self):
        if self.idx < self.size:
            item = self.func(self.iterables[self.idx])
            self.idx += 1
            return item
        else:
            raise StopIteration


def main():
    res = Map_.map(square, [1, 2, 3, 4, 5, 6])
    print("square value: {}".format(list(res)))


if __name__ == '__main__':
    main()
