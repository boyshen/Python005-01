# -*- encoding: utf-8 -*-
"""
@file: urls.py
@time: 2021/1/11 上午10:54
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

# urlpatterns = [
#     path('snippets/', views.SnippetsViewSet.as_view()),
#     path('snippets/<int:pk>', views.SnippetsDetail.as_view()),
#     path('users/', views.UserList.as_view()),
#     path('users/<int:pk>/', views.UserDetail.as_view()),
#     path('', views.api_root),
#     path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view()),
# ]
# urlpatterns = [
#     path('snippets/', views.snippet_list)
# ]

urlpatterns = [
    path('', views.api_root),
    path('snippets/', views.SnippetsViewSet.as_view(), name='snippet-list'),
    path('snippets/<int:pk>/', views.SnippetsDetail.as_view(), name='snippet-detail'),
    path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view(), name='snippet-highlight'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)
