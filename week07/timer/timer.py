# -*- encoding: utf-8 -*-
"""
@file: timer.py
@time: 2021/1/4 下午2:55
@author: shenpinggang
@contact: 1285456152@qq.com
@desc:  实现一个 @timer 装饰器，记录函数的运行时间，注意需要考虑函数可能会接收不定长参数。
"""
import functools
import time


# 装饰器
def timer(func):
    @functools.wraps(func)
    def wraps(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print("{} Function Running time: {:.2f} ms".format(func.__name__, (end - start) * 1000))
        return result

    return wraps


@timer
def test(num):
    for i in range(num):
        print("run count: {}".format(i))
        time.sleep(1)


def main():
    test(3)


if __name__ == '__main__':
    main()
