
from django.db import models

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=128)
    p_type = models.CharField(max_length=128)

class Book(models.Model):
    name = models.CharField(max_length=128)
    auther = models.CharField(max_length=128)
    puplisher = models.CharField(max_length=128)
    genre = models.CharField(max_length=128)
