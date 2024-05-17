from django.db import models

# Create your models here.
# verification/models.py

from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')


class UserDetails(models.Model):
    f_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)  # You need to specify max_length for CharField
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)
