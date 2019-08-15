from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser,models.Model):
    name=models.CharField(max_length=30)
    role=models.CharField(max_length=30)
    company=models.CharField(max_length=30)
    phone=models.CharField(max_length=30)
    employees=models.CharField(max_length=30)
    email=models.CharField(max_length=50)


class AssetModel(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    asset_name=models.CharField(max_length=50)


class EmployeeProfile(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='profile/',default='ig.png')
    role=models.CharField(max_length=200)
    Phone=models.CharField(max_length=200)
    kra=models.CharField(max_length=200)
    id_no=models.CharField(max_length=200)
    dob=models.DateField()

class Notifications(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    message=models.CharField(max_length=225)
    created_at=models.DateTimeField(auto_now=True)
    status=models.BooleanField(default=False)
    class Meta:
        ordering=['-created_at']

    def __str__(self):
        return self.message
