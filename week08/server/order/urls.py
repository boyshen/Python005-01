# -*- encoding: utf-8 -*-
"""
@file: urls.py
@time: 2021/1/12 下午4:59
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""

from django.urls import path, include

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

from order import views

order_list = views.OrderViewSet.as_view({
    'get': 'list'
})

order_create = views.OrderViewSet.as_view({
    'post': 'create'
})

order_detail = views.OrderViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

order_cancel = views.OrderViewSet.as_view({
    'get': 'cancel',
})

# router = DefaultRouter()
# router.register(r'order/create', views.OrderViewSet.create)
# router.register(r'order', views.OrderViewSet)

urlpatterns = [
    # path('', include(router.urls))
    path('', views.api_root),
    path('order', order_list, name='order-list'),
    path('order/<int:pk>', order_detail, name='order-detail'),
    path('order/create', order_create, name='order-create'),
    path('order/<int:pk>/cancel', order_cancel, name='order-cancel'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
