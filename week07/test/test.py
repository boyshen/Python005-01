# -*- encoding: utf-8 -*-
"""
@file: test.py
@time: 2021/1/2 下午7:21
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""


def decorate(func):
    print("run ...")

    def inner(*args, **kwargs):
        return func(*args, **kwargs)

    return inner


@decorate
def function():
    pass
