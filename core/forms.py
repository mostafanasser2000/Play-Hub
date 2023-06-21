from typing import Any, Dict
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import  Playground
from django.utils.translation import gettext_lazy as _
import re 
from django.core.exceptions import ValidationError
from .models import Playground
from django.db.models import Q

class PlaygroudnForm(forms.ModelForm):
    name = forms.CharField(help_text='name should consist of characters only',label='', required=False,widget=forms.TextInput(attrs={
        'placeholder': 'Playgroud Name',
        'class': 'form-control', 
    }))
    
    city = forms.CharField(label='',required=False,widget=forms.TextInput(attrs={
        'placeholder': 'Playgroud City',
        'class': 'form-control'
    }))
    
    address = forms.CharField(label='',widget=forms.TextInput(attrs={
        'placeholder': 'Playgroud Address',
        'class': 'form-control'
    }))
    
   
    image = forms.ImageField(label='Choose an image for Playground',widget=forms.FileInput(attrs={
        'class': 'form-control form-control-sm',
        
    }))
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        if name  == "":
            raise ValidationError(_("the name field is  blank"),
                                  code="name_blank")
        if re.match(r"[A-Za-z]+", name) is None:
            raise forms.ValidationError(_("Playground name should consist of characters only")
                                  , code='invalid_name')
        return name
    
    def clean_city(self):
        city = self.cleaned_data.get('city')
        
        if city  == "":
            raise forms.ValidationError(_("the city field is  blank"),
                                  code="city_blank")
        if re.match(r"^[A-Za-z]+$", city) is None:
            raise forms.ValidationError(_("city name should consist of characters only")
                                  , code='invalid_city')
        return city
        

    class Meta:
        model = Playground
        fields = ['name','city', 'address','capcity', 'grass_type','image']
        
       
        widgets = {
            'capcity': forms.RadioSelect(),
            'grass_type': forms.RadioSelect()
        }


        


