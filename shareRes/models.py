from django.db import models


# Create your models here.

class Category(models.Model):
    label = models.CharField(max_length=256)


class Restaurant(models.Model):
    name = models.CharField(max_length=256)
    link = models.CharField(max_length=500, null=True)
    content = models.TextField(null=True)
    keyword = models.CharField(max_length=256, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)
