# -*- encoding: utf-8 -*-
"""
@file: converters.py
@time: 2020/12/12 下午5:09
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""


class IntConvert(object):
    """
    匹配 URL 变量规则。整数规则
    """
    # 正则表达式
    regex = '[0-9]+'

    def to_python(self, value):
        """
        在 python 中使用，整数模式
        :param value:
        :return:
        """
        return int(value)

    def to_url(self, value):
        """
        在 url 中使用。字符串格式
        :param value:
        :return:
        """
        return str(value)


class FourDigitYearConvert(object):
    """
    匹配 URL 中四个数字的年份
    """
    # 正则表达式
    regex = '[0-9]{4}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)
