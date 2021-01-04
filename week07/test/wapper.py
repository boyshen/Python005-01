# -*- encoding: utf-8 -*-
"""
@file: wapper.py
@time: 2021/1/3 上午11:23
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""
import functools


def decorator(_class):
    class Count(object):
        def __init__(self, *args, **kwargs):
            self.time = 0
            self.wrapped = _class(*args, **kwargs)

        def display(self):
            # 重写传入类中的 display 方法
            self.time += 1
            print("{} run time: {}".format(_class, self.time))
            self.wrapped.display()
    # 返回新的 class 。
    return Count


@decorator
class Test(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def display(self):
        print("a = {}, b = {}".format(self.a, self.b))


def main():
    t = Test(1, b=4)
    # 输出：<class '__main__.Test'> run time: 1, a = 1, b = 4
    t.display()
    # 输出：<class '__main__.Test'> run time: 2, a = 1, b = 4
    t.display()
    # 输出：<class '__main__.decorator.<locals>.Count'>
    print(t.__class__)
    # 输出：<class 'type'> Count
    # 注意这里的类名不在是 Test。
    print(Test.__class__, Test.__name__)


if __name__ == '__main__':
    main()
