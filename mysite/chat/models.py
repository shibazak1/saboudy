from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Message(models.Model):

    text = models.CharField(max_length=129)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)

    created_at = models.DateTimeField(auto_now=True)
    
