from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.

class User(AbstractUser):

    def __str__(self):
        return self.first_name

class Profile(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)
    last_use_date = models.DateField(default=datetime.now)
    counter = models.PositiveIntegerField(default=5)
    