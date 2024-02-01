from django import forms
from .models import Playground, Attachment
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import Playground
from django.db.models import Q


class PlaygroundForm(forms.ModelForm):
    name = forms.CharField(
        help_text="name should consist of characters only",
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Playground Name",
                "class": "form-control",
                "autocomplete": "off",
            }
        ),
    )

    city = forms.Select()

    image = forms.ImageField(
        label="Choose an image for Playground",
        widget=forms.FileInput(
            attrs={
                "class": "form-control form-control-sm",
            }
        ),
    )
    capacity = forms.RadioSelect()
    grass_type = forms.RadioSelect()

    class Meta:
        model = Playground
        fields = [
            "name",
            "city",
            "capacity",
            "grass_type",
            "image",
        ]

    def clean(self):
        data = self.cleaned_data
        name = data.get("name")
        city = data.get("city")

        if Playground.objects.exclude(id=self.instance.id).filter(
            Q(name=name) & Q(city=city)
        ):
            raise forms.ValidationError(
                "Playground with this name and city already exist"
            )
        return data


# allow owners to add multiple images to playground
# class PlaygroundImageForm(PlaygroundForm):
#     file = forms.FileField(widget=forms.ClearableFileInput(attrs={"multiple": True}))

#     class Meta(PlaygroundForm.Meta):
#         fields = PlaygroundForm.Meta.fields + [
#             "file",
#         ]
