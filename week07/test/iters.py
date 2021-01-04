# -*- encoding: utf-8 -*-
"""
@file: iters.py
@time: 2021/1/3 下午5:31
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""


def test():
    _dict = {'a': 1, 'b': 2}
    iter_dict = iter(_dict)

    # 输出 key： a
    print(next(iter_dict))

    _dict['c'] = 3
    # RuntimeError 报错。字典迭代，字典有新的插入后，迭代器会立即失效。
    print(next(iter_dict))


def test1():
    _list = [1, 2, 3]
    iter_list = iter(_list)

    print(next(iter_list))

    _list.append(4)
    # 不会报错。尾插入不会导致迭代器损坏。列表会自动变长
    print(next(iter_list))
    print(next(iter_list))
    print(next(iter_list))


def jumpy_range(size):
    index = 0
    while index < size:
        jumpy = yield index
        print("jumpy : ", jumpy)
        if jumpy is None:
            jumpy = 1
        index += jumpy
        print("index: ", index)


def main():
    jumpy_iter = jumpy_range(5)
    # 输出 0
    print(next(jumpy_iter))
    # 输出 2. send 传入参数的同时也进行一次取值。
    print(jumpy_iter.send(2))
    # 输出 3
    print(next(jumpy_iter))
    # 输出 4
    print(next(jumpy_iter))
    # StopIteration 异常
    print(next(jumpy_iter))

    # test1()


if __name__ == '__main__':
    main()
