# -*- encoding: utf-8 -*-
"""
@file: mixin_ .py
@time: 2020/12/27 下午4:49
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""


class Displayer(object):
    def display(self, message):
        print(message)


class LoggerMixin(object):
    """
    Mixin 类
    """

    def log(self, message, filename='logfile.txt'):
        with open(filename, 'a') as fh:
            fh.write(message)

    def display(self, message):
        # 混合其他类进行使用。
        super().display(message)
        self.log(message)


class MySubClass(LoggerMixin, Displayer):
    def log(self, message):
        super().log(message, filename='subclasslog.txt')


def main():
    subclass = MySubClass()
    print(MySubClass.mro())
    subclass.display("This string will be shown and logged in subclasslog.txt")


if __name__ == '__main__':
    main()
