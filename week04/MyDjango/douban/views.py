from django.shortcuts import render
from django.http import HttpResponseNotFound
from .models import Movie, Comment


# Create your views here.

def movie_comment(request, mid):
    """
    返回指定电影的评论、星级、日期
    """
    query_set = Movie.objects.filter(mid=mid)
    if len(query_set) == 0:
        return HttpResponseNotFound("404 页面没有发现，检查输入的URL是否正确")

    # 电影名
    movie_name = query_set[0].name

    # 评论
    comment = Comment.objects.filter(mid=mid)
    for item in comment:
        item.date = item.date.strftime('%Y-%m-%d')

    return render(request, 'index.html', locals())


def movie_comment_by_star(request, mid, star):
    """
    返回指定电影评论中，星级大于 star 的信息
    """
    query_set = Movie.objects.filter(mid=mid)
    if len(query_set) == 0:
        return HttpResponseNotFound("404 页面没有发现，检查输入的URL是否正确")

    # 电影名
    movie_name = query_set[0].name

    # 评论
    comment = Comment.objects.filter(mid=mid, star__gt=star)
    for item in comment:
        item.date = item.date.strftime('%Y-%m-%d')
    return render(request, 'index.html', locals())
