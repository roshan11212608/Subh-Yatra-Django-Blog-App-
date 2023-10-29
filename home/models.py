from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    picture=models.ImageField(upload_to="profiles/")
    picturename=models.CharField(max_length=200,null=True,blank=True)
    
class Blog(models.Model):
    username=models.TextField()
    title=models.CharField(max_length=200)
    content=models.TextField()
    picture=models.ImageField(upload_to='vlogsimage/')
    vlogpicturename=models.CharField(max_length=200,null=True,blank=True)
class Contact(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField(max_length=200)
    message=models.TextField()
    