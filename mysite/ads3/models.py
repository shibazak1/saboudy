from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

class MyUser(AbstractUser):

    pass


    def __str__(self):

        return self.username
    







class Tage(models.Model):
    name = models.TextField()


    def __str__(self):
        return self.name
     


class Ad3(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    text = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    
    favourites = models.ManyToManyField(settings.AUTH_USER_MODEL,through="Favourite",related_name="favourite_ads")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,through="Coment",related_name="comments_owner")
   # tags = models.ManyToManyField(Tage,through="Ad_Tage",related_name="tage_ad")
    tag = models.ManyToManyField(Tage,through="Ad_Tage",related_name="tage_ad")
    
    
    
    

     # Picture
    picture = models.BinaryField(null=True, blank=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, blank=True,
        help_text='The MIMEType of the file')

    # Shows up in the admin list
    def __str__(self):
        return self.title


class Coment(models.Model):

    text = models.CharField(max_length=200,
                            validators=[MinLengthValidator(2,"write more lazy")])

    ad = models.ForeignKey(Ad3,on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):

        if len(self.text)<15:
            return self.text
        return self.text[:16]+"....."



class Favourite(models.Model):

    ad = models.ForeignKey(Ad3,on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('ad','owner')



    def __str__(self):

        return f"{self.user.username} like {self.ad.title[:10]}"
    
    
class Ad_Tage(models.Model):

    ad = models.ForeignKey(Ad3,on_delete=models.CASCADE)
    tage = models.ForeignKey(Tage,on_delete=models.CASCADE)


    

class Cart(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def total_price(self):

        total = 0
        items = CartItem.objects.filter(cart=self)

        for item in items:
            total += item.price*item.quantity

        return total
    
            


class CartItem(models.Model):

    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Ad3,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price  = models.DecimalField(max_digits=10,decimal_places=2,null=True)





    

class Order(models.Model):

    PENDING = 'PE'
    PROCESSING = 'PR'
    SHIPPED = 'SH'
    DELIVERED = 'DE'
    CANCELLED = 'CA'
    RETURNED = 'RE'

    ORDER_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled'),
        (RETURNED, 'Returned'),
    ]


    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    delivery_cost = models.DecimalField(max_digits=10,decimal_places=2)
    total = models.DecimalField(max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=ORDER_STATUS_CHOICES,default=PENDING,)

    
    longitude = models.DecimalField(max_digits=9,decimal_places=6,blank=True,null=True)
    latitude = models.DecimalField(max_digits=9,decimal_places=6,blank=True,null=True)




class OrderItem(models.Model):

    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Ad3,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    






class Driver(MyUser):

    vehicle_detail = models.CharField(max_length=200)
    license_number = models.CharField(max_length=50,unique=True)
    is_available = models.BooleanField(default=True)

    
    longitude = models.DecimalField(max_digits=9,decimal_places=6,blank=True,null=True)
    latitude = models.DecimalField(max_digits=9,decimal_places=6,blank=True,null=True)





    class Meta:

        verbose_name_plural = "Driver"

        
    def __str__(self):
        return f"Driver : {self.username}"
    


class DriverOrder(models.Model):

    driver = models.ForeignKey(Driver,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    picked_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True,blank=True)

    status =  models.CharField(max_length=20 ,choices=[("Picked","Picked"),
                                                        ("In Transit","In Transit"),
                                                       ("Delivered","Delivered"),],default="Picked")

    
    def total_money(self,driver):

        total = 0

        obje =  DriverOrder.objects.filter(driver=driver)

        for item in obje:
            total +=item.order.total_amount
        return total
    
