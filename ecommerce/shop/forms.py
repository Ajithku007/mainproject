from symtable import Class

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from shop.models import Category


class Registerform(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2','email']


class Loginform(forms.Form):
    username=forms.CharField(max_length=30)
    password=forms.CharField(widget=forms.PasswordInput)


class categoryform(forms.ModelForm):
    class Meta:
        model=Category
        fields='__all__'

from shop.models import Product
class Productform(forms.ModelForm):
    class Meta:
        model=Product
        fields=["name","image","description","price","stock","category"]

class Stockform(forms.ModelForm):
    class Meta:
        model=Product
        fields=["stock"]


