from django.db import models

# Create your models here.

class Concert(models.Model):
    name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    data = models.DateTimeField()
    