# -*- encoding: utf-8 -*-
"""
@file: main.py
@time: 2020/12/27 下午12:03
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""
# 导入其他模块
from week06.test import Word


# Word 模块
# class Word(object):
#     def __init__(self):
#         self.a = 1
#         self.b = 2
#
#
# def run():
#     w = Word()
#     print(id(w), w.a, w.b)

# 运行
def main():
    # 输出
    # 4426132448 1 2
    # 4426132448 1 2
    Word.run()
    Word.run()


if __name__ == '__main__':
    main()
