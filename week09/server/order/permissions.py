# -*- encoding: utf-8 -*-
"""
@file: permissions.py
@time: 2021/1/12 下午6:07
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""
from rest_framework import permissions


class IsCreateListUpdateDelete(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        # 更新和删除权限仅允许当前登录用户操作。
        return obj.owner == request.user
