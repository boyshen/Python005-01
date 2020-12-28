# -*- encoding: utf-8 -*-
"""
@file: single2.py
@time: 2020/12/27 上午11:01
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""


class TestCase(object):
    __instance = False

    def __new__(cls, *args, **kwargs):
        if cls.__instance:
            return cls.__instance
        cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        print("Test case")
        self.a = 1
        print("test init")


def main():
    test1 = TestCase()
    test2 = TestCase()
    print(id(test1), test1.a)
    print(id(test2), test2.a)


if __name__ == '__main__':
    main()
