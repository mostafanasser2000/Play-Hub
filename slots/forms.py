from django import forms
from .models import Slot
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.db.models import Q
import datetime


class SlotForm(forms.ModelForm):
    day = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
                "min": datetime.date.today(),
                "max": datetime.date.today() + datetime.timedelta(weeks=1),
            }
        )
    )
    start_hour = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                "class": "form-control",
                "type": "time",
            }
        )
    )

    end_hour = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                "class": "form-control",
                "type": "time",
            }
        )
    )
    price = forms.IntegerField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Price",
                "class": "form-control",
                "type": "number",
                "autocomplete": "off",
            },
        ),
    )

    class Meta:
        model = Slot
        fields = ["day", "start_hour", "end_hour", "price", "playground"]

        widgets = {
            "playground": forms.Select(
                attrs={
                    "class": "form-select",
                }
            )
        }

    def clean_day(self):
        day = self.cleaned_data["day"]
        if day is None or (
            day < datetime.date.today()
            or day > datetime.date.today() + datetime.timedelta(weeks=1)
        ):
            raise ValidationError("invalid day")

        return day

    def clean_end_hour(self):
        start_hour = self.cleaned_data.get("start_hour")
        end_hour = self.cleaned_data.get("end_hour")
        if end_hour < start_hour:
            raise forms.ValidationError(_("End hour must be greater than start hour"))

        if (
            start_hour.minute != 0
            or start_hour.second != 0
            or end_hour.minute != 0
            or end_hour.second != 0
        ):
            raise forms.ValidationError(
                _("Slots must have full-hour start and end times")
            )
        return end_hour

    def clean_price(self):
        price = self.cleaned_data["price"]

        if price is None or price < 0:
            raise ValidationError("Slot price must be greater than 0")
        return price

    def save(self, commit=True):
        slot = super().save(commit=False)

        day = slot.day
        start_hour = slot.start_hour
        end_hour = slot.end_hour
        playground = slot.playground

        if Slot.objects.exclude(id=self.instance.id).filter(
            Q(playground=playground)
            & Q(day=day)
            & Q(start_hour=start_hour)
            & Q(end_hour=end_hour)
        ):
            raise forms.ValidationError(
                "Slots with this information already exist",
            )

        if commit:
            slot.save()
        return slot
