# -*- encoding: utf-8 -*-
"""
@file: serializer.py
@time: 2021/1/12 下午4:40
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""

from rest_framework import serializers
from order.models import Order
from django.contrib.auth.models import User


# class OrderSerializer(serializers.ModelSerializer):
#     owner = serializers.ReadOnlyField(source='owner.username')
#
#     class Meta:
#         model = Order
#         fields = ['created', 'owner', 'commodity', 'status', 'remarks']
#
#
# class UserSerializer(serializers.ModelSerializer):
#     order = serializers.PrimaryKeyRelatedField(many=True, queryset=Order.objects.all())
#
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'order']

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    cancel = serializers.HyperlinkedIdentityField(view_name='order-cancel')

    class Meta:
        model = Order
        fields = ['url', 'id', 'created', 'owner', 'commodity', 'status', 'remarks', 'cancel']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    order = serializers.HyperlinkedRelatedField(many=True, view_name='order-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'order']
