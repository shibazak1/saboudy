from django import forms
from django.core.exceptions import ValidationError
from django.core import validators

class BookForm(forms.Form):
    name = forms.CharField(validators=[
        validators.MinLengthValidator(2, "Please enter 2 or more characters")])
    author = forms.CharField(validators=[
        validators.MinLengthValidator(2, "Please enter 2 or more characters")])
    poplisher = forms.CharField(validators=[
        validators.MinLengthValidator(2, "Please enter 2 or more characters")])
    gnere = forms.CharField(validators=[
        validators.MinLengthValidator(2, "Please enter 2 or more characters")])


class crispy(forms.Form):
    care_name = forms.CharField(validators=[validators.MinLengthValidator(2,"Pleas enter 2 or more token")])
    model = forms.IntegerField()

    
