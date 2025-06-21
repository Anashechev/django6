from django import forms
from .models import Clothes

class ClothesForm(forms.ModelForm):
    
    class Meta:
        model = Clothes
        fields = ['name', 'description', 'price',
                   'size', 'color', 'photo', 
                   'is_exist', 'category', 'collection']