from django.core.validators import RegexValidator

from django.db import models

# Create your models here.

class Contact(models.Model):        
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15,unique=True)
    address = models.TextField()