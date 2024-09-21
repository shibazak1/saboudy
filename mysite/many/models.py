from django.db import models

# Create your models here.

class book(models.Model):
    name = models.CharField(max_length=29)
    authors = models.ManyToManyField("author",
                               through="authored")
    




class author(models.Model):
    name  = models.CharField(max_length=29)
    books = models.ManyToManyField("book",through="authored")




class authored(models.Model):
    book = models.ForeignKey(book,
                             on_delete=models.CASCADE)
    author = models.ForeignKey(author,
                               on_delete=models.CASCADE
                            )
    
    
#------------------------------------------------------------------------------

class person(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    courses = models.ManyToManyField("course",through="membership")


class course(models.Model):
    title = models.CharField(max_length=20)
    members = models.ManyToManyField("person",through="membership")



class membership(models.Model):
    person = models.ForeignKey(person,on_delete=models.CASCADE)
    course = models.ForeignKey(course,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    LEARNER = 1
    IA  =100
    INSTRUCTER = 200
    ADMIN = 500


    member_choice = (

        (LEARNER,"learner"),
        (IA,"Instrucureal assestent"),
        (INSTRUCTER,"instructer"),
        (ADMIN,"admin"),

    )

    role = models.IntegerField(choices=member_choice,default=LEARNER)
    
