# -*- encoding: utf-8 -*-
"""
@file: single.py
@time: 2020/12/27 上午10:49
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""


# 装饰器
def single(cls):
    instance = {}

    def get_instance():
        if cls not in instance:
            instance[cls] = cls()
        return instance[cls]

    return get_instance


@single
class TestClass(object):
    # 单例模式下，传入参数没有实际意义。因为只会返回第一次创建的实例。
    # 如果传入参数，第二次创建传入的参数，则不会被初始化使用
    def __init__(self):
        print("test class")


def main():
    test1 = TestClass()
    test2 = TestClass()
    print(id(test1))
    print(id(test2))


if __name__ == '__main__':
    main()
