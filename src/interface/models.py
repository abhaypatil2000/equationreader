from django.db import models

# Create your models here.
class CommonBooks(models.Model):
    name = models.CharField(max_length=100)
    pdf = models.FileField()
    audio = models.FileField()

    def __str__(self):
        return self.name

    class Meta:
        ordering =  ['name']