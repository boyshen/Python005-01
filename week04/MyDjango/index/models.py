from django.db import models


# Create your models here.
# 图书or电影
# class Type(models.Model):
#     # id = models.AutoField(primary_key=True)  # Django会自动创建,并设置为主键
#     typename = models.CharField(max_length=20)
#
#
# 作品名称和作者(主演)
class MovieName(models.Model):
    # id 自动创建
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    stars = models.CharField(max_length=10)


class User(models.Model):
    # id 自动创建
    username = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    # stars = models.CharField(max_length=10)


class Audit(models.Model):
    transfer_uid = models.CharField(max_length=128)
    receivable_uid = models.CharField(max_length=128)
    money = models.SmallIntegerField()
    update_time = models.DateTimeField()

    # 元数据类。不属于任何一个字段的数据。
    class Meta:
        # 通常为 False，指定对反向映射的表结构不进行修改
        managed = False
        # 映射的表名称
        db_table = 'audit'
