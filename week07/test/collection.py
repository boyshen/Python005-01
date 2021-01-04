# -*- encoding: utf-8 -*-
"""
@file: collection.py
@time: 2021/1/3 下午12:53
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""


class Test(object):
    def __init__(self):
        pass

    def __setitem__(self, key, value):
        print("set item ", key, value)

    def __getitem__(self, item):
        print("get item ", item)

    def __iter__(self):
        return iter([i for i in range(10)])


# type hint(类型注解)。静态模式。声明传入的变量类型和返回的变量类型。如果传入的类型不对，在 IDE 中会有提示
def test(text: str, number: int) -> str:
    print(text)
    print(number)
    return "ok"


def main():
    test("hello", 2)
    # 提示传入的类型不对
    test(1, 2)

    # a = "hello world"
    # # 使用f-string模式。输出: hello world, 3 * 4 = 12
    # print(f"{a}, 3 * 4 = {3 * 4}")

    # t = Test()
    # # 调用 setitem
    # t['z'] = 1
    # # 调用 getitem
    # val = t['z']
    #
    # # 调用 iter
    # for i in t:
    #     print(i)


if __name__ == '__main__':
    main()
