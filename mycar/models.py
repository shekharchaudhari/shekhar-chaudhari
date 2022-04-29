
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

class Trip(models.Model):
    users = models.ForeignKey(User,on_delete=models.CASCADE,null=True)  
    pick_loc = models.CharField(max_length=30)
    drop_loc = models.CharField(max_length=30)
    p_date = models.CharField(null=True,max_length=15)
    d_date = models.CharField(null=True,max_length=15)
    pick_time = models.CharField(max_length=10)
    
    def __str__(self):
        return self.pick_loc  

class Car(models.Model):
    car_type = models.CharField(max_length=30)
    car_pic = models.FileField(upload_to='cars')
    p_hour = models.IntegerField(default=0)
    p_day = models.IntegerField(default=0)
    fuel_type = models.CharField(max_length=10)        

    def __str__(self):
        return self.car_type  

class Book(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip,on_delete=models.CASCADE)
    car = models.ForeignKey(Car,on_delete=models.CASCADE)
    amount = models.IntegerField()
    pay_id = models.CharField(max_length=50,null=True,blank=True)
    verify = models.BooleanField(default=False)
    at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email