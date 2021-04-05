from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    last_use_date = models.DateField(default=timezone.now)
    counter = models.PositiveIntegerField(default=5)
    def __str__(self):
        return self.username