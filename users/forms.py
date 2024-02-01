from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(
        label="",
        max_length=255,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email Address",
                "autocomplete": "off",
            }
        ),
    )
    first_name = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "autocomplete": "off",
            }
        ),
    )
    last_name = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "autocomplete": "off",
            }
        ),
    )
    phone_number = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Phone Number",
                "autocomplete": "off",
            }
        ),
    )
    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "autocomplete": "off",
            }
        ),
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password confirmation",
                "autocomplete": "off",
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "role",
            "phone_number",
            "password1",
            "password2",
        ]

    def clean_email(self):
        """Verify email is taken"""
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")

        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminCreationForm(forms.ModelForm):
    """Form for creating users."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ("email", "role")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """Form for updating users, including all fields on the user"""

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("email", "role", "is_active", "is_admin")

    def clean_password(self):
        return self.initial["password"]
