from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .forms import UserAdminCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()
admin.site.unregister(Group)


class UserAdmin(BaseUserAdmin):
    add_form = UserAdminCreationForm  # the form to add user instance
    form = UserChangeForm  # the form to change user instance

    # The fields to be used in displaying the User model
    # These override the def
    list_display = (
        "first_name",
        "last_name",
        "email",
        "role",
        "phone_number",
        "is_admin",
    )
    list_filter = ("is_admin", "role")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "role",
                )
            },
        ),
        (
            "Permissions",
            {"fields": ("is_admin",)},
        ),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. User Admin
    # overrides get_fieldsets to use this attribute when creating user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "email",
                    "role",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    search_fields = ("email", "first_name", "last_name", "phone_number")
    ordering = (
        "first_name",
        "last_name",
        "email",
    )
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
