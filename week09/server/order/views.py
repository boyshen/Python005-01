from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import renderers
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import renderers

from order.models import Order
from order.serializer import OrderSerializer
from order.serializer import UserSerializer
from order.permissions import IsCreateListUpdateDelete


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCreateListUpdateDelete]

    @action(methods=['GET'], detail=True)
    def cancel(self, request, pk, *args, **kwargs):
        try:
            order = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            raise Http404

        if order.cancel and order.status == 'Cancelled':
            return Response(status=status.HTTP_200_OK)

        order.status = 'Cancelled'
        order.cancel = True
        order.save()
        return Response(status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        print(self.request.user == User)
        serializer.save(owner=self.request.user)


# class OrderList(generics.ListCreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCreateListUpdateDelete]
#
#     def perform_create(self, serializer):
#         print(self.request.user == User)
#         serializer.save(owner=self.request.user)


# class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCreateListUpdateDelete]


# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class OrderCancel(APIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCreateListUpdateDelete]
#
#     def get(self, request, pk, format=None):
#         try:
#             order = Order.objects.get(id=pk)
#         except Order.DoesNotExist:
#             raise Http404
#
#         if order.cancel and order.status == 'Cancelled':
#             return Response(status=status.HTTP_200_OK)
#
#         order.status = 'Cancelled'
#         order.cancel = True
#         order.save()
#         return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'order': reverse('order-list', request=request, format=format),
    })
