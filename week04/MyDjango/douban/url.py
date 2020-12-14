# -*- encoding: utf-8 -*-
"""
@file: url.py
@time: 2020/12/14 下午3:03
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""

from django.urls import path
from . import views

urlpatterns = [
    # 显示指定电影的所有评论
    # http://127.0.0.1:8888/douban/mid=7e2c3043-59d8-49f4-9aee-6de90ce232ce
    # mid=7e2c3043-59d8-49f4-9aee-6de90ce232ce 为电影的 id
    path('mid=<str:mid>', views.movie_comment),

    # 指定 star 进行显示。
    # 例如 http://127.0.0.1:8888/douban/mid=7e2c3043-59d8-49f4-9aee-6de90ce232ce/star=3
    # mid=7e2c3043-59d8-49f4-9aee-6de90ce232ce 为电影的 id
    # star=3。表示显示 3 星级以上的评论。不包括 3 星级。
    path('mid=<str:mid>/star=<int:star>', views.movie_comment_by_star)
]
