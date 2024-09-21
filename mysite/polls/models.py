from django.db import models

# Create your models here.

class Product_Item(models.Model):
    name  = models.CharField(max_length=128)
    price = models.FloatField()
    


    
