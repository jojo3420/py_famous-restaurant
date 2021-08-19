from django.db import models


# Create your models here.
class Category(models.Model):
    label = models.CharField(max_length=50)


class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=250)
    content = models.TextField()
    keyword = models.CharField(max_length=100)
    category = models.ForeignKey(Category, default=1, on_delete=models.SET_DEFAULT)
