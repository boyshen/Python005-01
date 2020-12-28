# -*- encoding: utf-8 -*-
"""
@file: factory1.py
@time: 2020/12/27 下午12:34
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""


class Human(object):
    def __init__(self, gender):
        self.gender = gender

    def get_gender(self):
        return self.gender


class Man(Human):
    def __init__(self, name, gender):
        super(Man, self).__init__(gender)
        self.name = name

    def get_name(self):
        return self.name


class Woman(Human):
    def __init__(self, name, gender):
        super(Woman, self).__init__(gender)
        self.name = name

    def get_name(self):
        return self.name


class Factory(object):
    def get_human(self, gender, name):
        if gender == 'M':
            return Man(gender, name)
        elif gender == 'F':
            return Woman(gender, name)
        else:
            pass
