from django.shortcuts import render
from django.http import HttpResponse
from . import models


# Create your views here.

def index(request):
    return HttpResponse("hello world")


# 对应 url 中 path('<int:year>', views.my_year)
def my_year(request, year):
    return HttpResponse(year)


# 如果是多个参数，可以使用 **kwargs 方式代替。
# def my_year_name(request, **kwargs):
#   name = kwargs['name']
# 对应 url 中 path('<int:year>/<str:name>', views.my_year_name)
def my_year_name(request, year, name):
    return HttpResponse('year:{}, name:{}'.format(year, name))


# 对应 url 中 re_path('(?P<year>[0-9]{4}).html', views.my_re_year, name='url_year')
def my_re_year(request, year):
    return HttpResponse(year)


def get_user(request):
    user = models.User.objects.all()
    # return render(request, 'user.html', {'user': user})
    return render(request, 'user.html', locals())
