from django.db import models
from datetime import date
# Create your models here.
class userreg(models.Model):
    fname = models.CharField(max_length=50)
    mobile = models.CharField (max_length=10)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    rights = models.CharField(default="user", max_length=255)

class product(models.Model):
    prid = models.CharField(max_length=30)
    prname = models.CharField(max_length=30)
    price = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='images/')

class cart(models.Model):
    slno = models.IntegerField()
    pname = models.CharField(max_length=40)
    rate = models.IntegerField()
    qty = models.IntegerField()
    total = models.IntegerField()
    userid = models.IntegerField()

class onlinemaster(models.Model):
    salesno = models.IntegerField()
    salesdate = models.DateField(default=date.today)
    userid = models.IntegerField()
    uname = models.CharField(max_length=30)
    shipment= models.CharField(max_length=300)
    phone = models.CharField(max_length=10)
    cardno = models.CharField(max_length=40)
    total = models.IntegerField()
    status = models.CharField(max_length=30, default='New Order')

class onlinesub(models.Model):
    salesno = models.IntegerField()
    slno =models.IntegerField()
    pname = models.CharField(max_length=40)
    rate = models.IntegerField()
    qty = models.IntegerField()
    total = models.IntegerField()

class feedback(models.Model):
    uname = models.CharField(max_length=50)
    ph= models.CharField(max_length=50)
    feed = models.CharField(max_length=550)

