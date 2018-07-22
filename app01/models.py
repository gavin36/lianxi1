from django.db import models

# Create your models here.

#用户
class User(models.Model):
    user=models.CharField(max_length=32)
    pwd=models.CharField(max_length=32)

#客户
class Customer(models.Model):
    name=models.CharField(max_length=32)
    age=models.IntegerField()
    email = models.CharField(max_length=32)
    company=models.CharField(max_length=32)