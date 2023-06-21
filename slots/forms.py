from typing import Any, Dict
from django import forms
from .models import Slot
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from core.models import Playground
import datetime

class DateInput(forms.DateInput):
    input_type = 'date'


class SlotForm(forms.ModelForm):

    day = forms.DateField(widget=forms.DateInput(
        attrs={
            'class': 'form-control',
            'type': 'date',
            'min': datetime.date.today(),
            'max': datetime.date.today() + datetime.timedelta(weeks=1),
        }
    ))
    start_hour = forms.TimeField(widget=forms.TimeInput(
        attrs={
            'class': 'form-control',
            'type': 'time',
            
        }
    ))
    
    end_hour = forms.TimeField(widget=forms.TimeInput(
        attrs={
            'class': 'form-control',
            'type': 'time',

        }
    ))
    price = forms.IntegerField(label='',widget=forms.NumberInput(attrs={
        'placeholder':'Price',
        'class': 'form-control',
        'type': 'number',
    }, ))
    
   
    def clean_day(self):
        day = self.cleaned_data['day']
        
        if day is None:
            raise forms.ValidationError("day field is empty")
        if day < datetime.date.today() or day > datetime.date.today() + datetime.timedelta(weeks=1):
            raise ValidationError(_("Slot  must start  be today or within a week"))
        return day
    
    def clean_end_hour(self):
        start_hour = self.cleaned_data.get('start_hour')
        end_hour = self.cleaned_data.get('end_hour')
        
        if end_hour < start_hour:
            raise forms.ValidationError(_("invalid end hour"))

        slot_duration = datetime.datetime.combine(datetime.date.today(),end_hour)-datetime.datetime.combine(datetime.date.today(),start_hour)
        
        #  check if slot duration less than one hour
        if slot_duration.seconds < 3600 :
            raise forms.ValidationError(_("Slot duration must be at least 1 hour"))
        
        if slot_duration.seconds > 3 * 3600 :
            raise forms.ValidationError(_("Slot duration must be at most 3 hours"))
                
        return end_hour   
        
    
    def clean_price(self):
        price = self.cleaned_data['price']
        
        if price <= 0:
            raise forms.ValidationError(_("Slot price must be greater than 0"))
        return price
    
    class Meta:
        model = Slot
        fields = ['day', 'start_hour', 'end_hour', 'price', 'playground']
        
        widgest = {
            'playground': forms.Select(attrs={
                'class': 'form-select',
            })
        }
   