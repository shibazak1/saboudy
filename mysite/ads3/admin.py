from django.contrib import admin
from ads3.models import MyUser , Driver,Ad3 ,ProductVaraint,Color,Size
# Register your models here.



class ColorAdmin(admin.ModelAdmin):
	list_display=('title','color_bg')
admin.site.register(Color,ColorAdmin)



class SizeAdmin(admin.ModelAdmin):
	list_display=('title',)
admin.site.register(Size,SizeAdmin)


# Product Attribute
class ProductVaraintAdmin(admin.ModelAdmin):
    list_display=('id','image','product','price','color','size')
admin.site.register(ProductVaraint,ProductVaraintAdmin)


admin.site.register(Ad3)
#admin.site.register(ProductVaraint)
admin.site.register(MyUser)
admin.site.register(Driver)





