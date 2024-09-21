from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import ModelForm
from django import forms
from .models import Ad
from .humanize import neutralize




class AdForm(ModelForm):

    max_upload_limit = 2 * 1024 * 1024
    max_upload_text = neutralize(max_upload_limit)


    picture = forms.FileField(required=False ,label= 'Upload File <='+max_upload_text)
    upload_field_name = 'picture'

    
    class Meta:
        model = Ad
        fields = ["title","text",'picture']



    def clean(self):
        cleaned_data = super().clean()
        picture  = cleaned_data.get("picture")

        if picture is None:
            print("no picture")
            return
        if len(picture)> self.max_upload_limit:
            self.add_error("picture","file must be <="+max_upload_text+"byte")




    def save(self ,commit=True):
        ad_object = super(AdForm,self).save(commit=False)

        pic_file = ad_object.picture

        if isinstance(pic_file,InMemoryUploadedFile):
            pic_byte = pic_file.read()
            ad_object.content_type = pic_file.content_type
            ad_object.picture = pic_byte

        if commit:
            ad_object.save()

        return ad_object
    
            
            

            
        
