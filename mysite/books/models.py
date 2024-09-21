from django.db import models
from django.core.validators import MinLengthValidator
# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=120,
                            validators=[MinLengthValidator(2,"Auther most at least 2 characters")])

    def __str__(self):
        #when you try to print the Auther object as string the name field is what will printed
        return self.name

class Book(models.Model):

    name = models.CharField(max_length=120,
                            validators = [MinLengthValidator(2,"Book name at least 2 characters")])
    author = models.ForeignKey("Author",on_delete=models.CASCADE,null=False)
    genre = models.CharField(max_length = 120)
    price  = models.IntegerField()
    
    
