from django import forms
from django.contrib.auth.models import User
from .models import Product


class ProductCreationForm(forms.ModelForm):
    name = forms.CharField(label='Product Name:', required=True, max_length=16, widget=forms.TextInput(attrs={'placeholder': 'Enter Name of Product.'}))
    description = forms.CharField(label='Description of Product:', required=True, max_length=80, widget=forms.TextInput(attrs={'placeholder': 'Describ the Product.'}))

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']