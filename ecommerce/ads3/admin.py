from django.contrib import admin
from ads3.models import MyUser , Driver, Ad3 ,ProductVaraint,Color,Size,Brand,Subscription
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin
# Register your models here.



class ColorAdmin(admin.ModelAdmin):
	list_display=('title','color_bg')
admin.site.register(Color,ColorAdmin)

#product

class ProductAdmin(admin.ModelAdmin):
    list_display=('id','title','brand','status','is_featured')
    list_editable=('status','is_featured')
admin.site.register(Ad3,ProductAdmin)


# Product Attribute
class ProductVaraintAdmin(admin.ModelAdmin):
    list_display=('id','image','product','price','color','size')
admin.site.register(ProductVaraint,ProductVaraintAdmin)




# managing driver registration in admin
class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = ['username', 'email', 'first_name', 'last_name', 'is_staff','vehicle_detail','license_number']  # Fields to display in the admin  # Add any other fields if necessary

class DriverChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Driver
        fields = '__all__'  # This will allow editing of all fields, including password


class DriverAdmin(UserAdmin):
    add_form = DriverCreationForm
    form = DriverChangeForm
    model = Driver

    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'vehicle_detail', 'license_number','phone_number']  # Fields to display in the admin

    # Add custom fields to add_fieldsets (for creating new drivers)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name',
                       'password1', 'password2', 'vehicle_detail', 'license_number','phone_number','is_staff'),
        }),
    )

    # Add custom fields to fieldsets (for editing existing drivers)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Driver details', {'fields': ('vehicle_detail', 'license_number','phone_number')}),  # Custom section for driver-specific fields
    )

admin.site.register(Driver, DriverAdmin)



#user registration in admin
class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = ('username', 'email','password','phone_number')  # Add any other fields if necessary

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = MyUser
        fields = '__all__'  # This will allow editing of all fields, including password

class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = MyUser

    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff','phone_number']  # Fields to display in the admin

    
    # Add custom fields to add_fieldsets (for creating new drivers)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',
                       'phone_number', 'is_staff'),
        }),
    )

    # Add custom fields to fieldsets (for editing existing drivers)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Driver details', {'fields': ('phone_number',)}),  # Custom section for driver-specific fields
    )



admin.site.register(MyUser, MyUserAdmin)







admin.site.register(Brand)
admin.site.register(Size)
admin.site.register(Subscription)







