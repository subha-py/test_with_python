from django.db import models

# Create your models here.

class List(models.Model):
    pass

class Item(models.Model):
    text=models.CharField(max_length=120)
    list=models.ForeignKey(List,default=None)

