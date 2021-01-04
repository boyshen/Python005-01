# -*- encoding: utf-8 -*-
"""
@file: wapper1.py
@time: 2021/1/3 上午11:47
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""


# 为函数添加属性
def attr(**kwargs):
    def decorate(f):
        for k in kwargs:
            setattr(f, k, kwargs[k])
        return f

    return decorate


@attr(a=1, b=2)
def test():
    pass


def main():
    # 输出 1，2
    print(test.a, test.b)
    print(test.__dir__())


if __name__ == '__main__':
    main()
