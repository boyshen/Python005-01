from django.db import models

# Create your models here.
COMMODITY_NAME = [('food', '食物'), ('book', '书'), ('clothes', '衣服'), ('software', '软件')]
STATUS_TYPE = [('Normal', '正常')]


class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    commodity = models.CharField(choices=COMMODITY_NAME, default='food', verbose_name="商品", max_length=100)
    remarks = models.TextField(verbose_name="备注", default='null')
    status = models.CharField(choices=STATUS_TYPE, default='Normal', verbose_name="状态", max_length=100)
    cancel = models.BooleanField(default=False)

    owner = models.ForeignKey('auth.User', related_name='order', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
