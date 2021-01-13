# -*- encoding: utf-8 -*-
"""
@file: urls.py
@time: 2021/1/10 下午4:58
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""

from django.urls import include, path
from rest_framework import routers
from quick_start import views

router = routers.DefaultRouter()
# 这里为注册的url地址。以及对应的相应视图。例如：http://127.0.0.1:8000/api/v1/users/
# 注意 users 后面需要加 '/' 
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
