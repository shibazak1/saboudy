from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.conf import settings
from .models import Ad3,Tage,Ad_Tage,MyUser
from .humanize import neutralize
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(required=True)
    phone_number = PhoneNumberField()  # Use the form field for phone numbers

    class Meta:
        model = MyUser
        fields = ["username","email","phone_number","password1","password2"]
        
        



class AdForm(ModelForm):

    max_upload_limit = 2 * 1024 * 1024
    max_upload_text = neutralize(max_upload_limit)


#    picture = forms.FileField(required=False ,label= 'Upload File <='+ max_upload_text)
 #   upload_field_name = 'picture'

    tag = forms.CharField(help_text="Enter tages separated by comma")
    
    class Meta:
        model = Ad3
        fields = ["title","text",'tag']

"""

    def clean(self):
        cleaned_data = super().clean()
        picture  = cleaned_data.get("picture")

        if picture is None:
            print("no picture")
            return
        if len(picture)> self.max_upload_limit:
            self.add_error("picture","file must be <="+self.max_upload_text+"byte")




    def save(self ,commit=True):
        ad_object = super(AdForm,self).save(commit=False)

        pic_file = ad_object.picture

        if isinstance(pic_file,InMemoryUploadedFile):
            pic_byte = pic_file.read()
            ad_object.content_type = pic_file.content_type
            ad_object.picture = pic_byte
        
        

        if commit:
            ad_object.save()
            #self.save_m2m()

        return ad_object
"""


class CommentForm(forms.Form):

    text  = forms.CharField(max_length=200)
    
