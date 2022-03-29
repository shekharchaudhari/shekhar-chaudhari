from django.db import models

# Create your models here.
class User(models.Model):
    uname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    mobile = models.CharField(max_length=13,null=True)
    address = models.TextField(null=True,blank=True)
    pic =  models.FileField(upload_to='profile',default='Avatar.png')

def __str__(self):
    return self.email
