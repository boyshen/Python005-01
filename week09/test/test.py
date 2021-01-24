# -*- encoding: utf-8 -*-
"""
@file: test.py
@time: 2021/1/11 下午2:50
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""
import sys
import traceback


def test():
    a = 1 / 0


def test1():
    test()


def main():
    try:
        test1()
    except Exception as e:
        print(e)
        _type, _val, _traceback = sys.exc_info()

        # 写入文件
        # with open('log.txt', 'a') as f:
        #     traceback.print_exc(file=f)

        # 格式化字符串输出
        exception = traceback.format_exception(_type, _val, _traceback)
        for i in exception:
            print(i.strip('\n'))


if __name__ == '__main__':
    main()
