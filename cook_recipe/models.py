from django.db import models
from accounts.models import CustomUser

class Stock(models.Model):
    user = models.ForeignKey(CustomUser,verbose_name='ユーザー',on_delete=models.PROTECT)
    product = models.CharField(verbose_name='商品',max_length=30)
    maker = models.CharField(verbose_name='製造業者',max_length=30,blank=True,null=True)
    sell_by = models.DateField(verbose_name='賞味期限',blank=True,null=True)
    update_at = models.DateTimeField(verbose_name='更新日時',auto_now_add=True)
    class Meta:
        verbose_name_plural = 'Stock'
    def __str__(self):
        return self.product