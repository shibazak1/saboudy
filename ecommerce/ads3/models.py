from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify

# this module handel phone number formate and validations
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

#my custom user
class MyUser(AbstractUser):

    phone_number = PhoneNumberField()

    
    def save(self, *args, **kwargs):
        if self.pk is None and not self.has_usable_password():
            # If it's a new user and the password isn't hashed, set the password properly
            self.set_password(self.password)
        super().save(*args, **kwargs)


    def __str__(self):

        return self.username
    
#color
class Color(models.Model):
    title=models.CharField(max_length=100)
    color_code=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural='4. Colors'

    def color_bg(self):
        return mark_safe('<div style="width:30px; height:30px; background-color:%s"></div>' % (self.color_code))

    def __str__(self):
        return self.title


# Size
class Size(models.Model):
    title=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural='5. Sizes'

    def __str__(self):
        return self.title

    

#tage model (category)
class Tage(models.Model):
    name = models.TextField()

    
    class Meta:
        verbose_name_plural='2. Category'



    def __str__(self):
        return self.name


# brand model for product
class Brand(models.Model):
    title = models.CharField(max_length=100)


    
    class Meta:
        verbose_name_plural='3. Brands'

        def __str__(self):
            return self.title
    

    

# product model
class Ad3(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )

    #slug is how the productappear in the search ex downy-gel
    slug = models.CharField(max_length=400)
    #description of the product
    text = models.TextField()
    # some specified detail about the product
    specs=models.TextField(blank=True,null=True)    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=True)
    favourites = models.ManyToManyField(settings.AUTH_USER_MODEL,through="Favourite",related_name="favourite_ads")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,through="Coment",related_name="comments_owner")
    tag = models.ManyToManyField(Tage,through="Ad_Tage",related_name="tage_ad")

    #does the product available 
    status=models.BooleanField(default=True)
    #does the product is spacial
    is_featured=models.BooleanField(default=False)

    
    class Meta:
        verbose_name_plural='1. Products'
        
    


    #create slug of the product from the title
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Automatically create a slug from the title
        super().save(*args, **kwargs)

        
    # Shows up in the admin list
    def __str__(self):
        return self.title


    
class ProductVaraint(models.Model):

    product = models.ForeignKey(Ad3,related_name="variants",on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    
    color  = models.ForeignKey(Color,on_delete=models.CASCADE)
    size  = models.ForeignKey(Size,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="product_imgs/",null=True)
    
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        
        return self.product.title
    


    



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
    product_variant = models.ForeignKey(ProductVaraint,on_delete=models.CASCADE)
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
    order = models.ForeignKey(Order,related_name="driverorder",on_delete=models.CASCADE)
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
    


#model to store the subscription info of user for pushing notification to them

class Subscription(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    auth_secret = models.TextField()
    key = models.TextField()
    endpoint = models.TextField()

    
