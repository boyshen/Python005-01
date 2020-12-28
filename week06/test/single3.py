# -*- encoding: utf-8 -*-
"""
@file: single3.py
@time: 2020/12/27 上午11:25
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""

import threading


class TestCase(object):
    __instance = None
    # 初始化线程锁
    locker = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls.__instance is not None:
            return cls.__instance

        # 获得锁
        cls.locker.acquire()
        try:
            if cls.__instance is None:
                cls.__instance = object.__new__(cls)
        except Exception as e:
            raise e
        finally:
            # 释放锁
            cls.locker.release()
            return cls.__instance

    def __init__(self):
        print("Test Case ...")
        self.a = 1


# class Test(TestCase):
#     def __init__(self):
#         super(Test, self).__init__()
#         print("Test ...")
#         self.b = 1


def main():
    test1 = TestCase()
    test2 = TestCase()
    print(id(test1), test1.a)
    print(id(test2), test2.a)


if __name__ == '__main__':
    main()
