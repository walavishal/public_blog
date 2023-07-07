from django.db import models
from django.utils import timezone
from datetime import timedelta
import os

# Create your models here.

class Myblog(models.Model):
    blog_id=models.CharField(max_length=300,primary_key=True)
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


class image(models.Model):
    blog_id=models.ForeignKey(Myblog,on_delete=models.CASCADE)
    image_path=models.ImageField(upload_to='Blog_Image',default="")

    def delete(self, *args, **kwargs):
        # Get the file path
        file_path = self.image_path.path

        # Delete the associated file if it exists
        if os.path.isfile(file_path):
            os.remove(file_path)

        # Call the parent's delete() method to delete the row from the database
        super().delete(*args, **kwargs)

