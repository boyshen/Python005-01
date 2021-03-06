# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    mid = models.CharField(max_length=128)
    star = models.IntegerField()
    comment = models.TextField()
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'comment'


class Movie(models.Model):
    mid = models.CharField(primary_key=True, max_length=128)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'movie'
