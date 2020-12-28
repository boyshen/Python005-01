# -*- encoding: utf-8 -*-
"""
@file: Word.py
@time: 2020/12/27 下午12:01
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""


class Word(object):
    def __init__(self):
        self.a = 1
        self.b = 2


def run():
    w = Word()
    print(id(w), w.a, w.b)
