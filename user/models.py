from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class Myblog(models.Model):
    topic=models.CharField(max_length=100)
    content=models.CharField(max_length=600)
    date=models.DateField(auto_now=True)
    email=models.CharField(max_length=600,default="")
    name=models.CharField(max_length=100,default="")
    time=models.TimeField(auto_now=True)

class usr(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=300)
    join_date=models.DateField(default=timezone.now().date())
    expiry_date=models.DateField(default=(timezone.now().date() + timedelta(days=30)))
    blog_view_count=models.IntegerField(default=0)
    premium=models.BooleanField(default=False)

