from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser,models.Model):
    name=models.CharField(max_length=30)
    role=models.CharField(max_length=30)
    company=models.CharField(max_length=30)
    phone=models.CharField(max_length=30)
    employees=models.CharField(max_length=30)
    email=models.CharField(max_length=50)
