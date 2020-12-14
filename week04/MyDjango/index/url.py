# -*- encoding: utf-8 -*-
"""
@file: url.py
@time: 2020/12/12 上午11:30
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""

from django.urls import path
from django.urls import re_path
from django.urls import register_converter
from . import views
from . import converters

# 注册转换函数。两个变量：转换函数名 和 url中替换名称
register_converter(converters.IntConvert, 'myint')

# register_converter(converters.FourDigitYearConvert, 'yyyy')

urlpatterns = [
    # path('', views.index),

    path('user', views.get_user),

    # 带变量的URL，类型模式.
    # int 表示类型。
    # year 表示需要传入到响应函数变量名。
    # views.my_year 响应函数。
    # 响应函数定义： def my_year(request, year):
    # 请求方式：http://127.0.0.1:8888/1
    #         http://127.0.0.1:8888/1/hello
    # path('<int:year>', views.my_year),
    # path('<int:year>/<str:name>', views.my_year_name),

    # 带变量的 URL. 正则表达式模式
    # 需要使用 from django.urls import re_path
    # 其中 ?P<year> 为指定的传入到响应函数的变量名, [0-9]{4} 为正则表达式
    # 响应函数定义：def my_re_year(request, year)
    re_path('(?P<year>[0-9]{4})', views.my_re_year),

    # 响应函数定义： def my_year(request, year):
    path('<myint:year>', views.my_year)

]
