from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomeUser
from .forms import CustomeUserChangeForm, RegisterForm


# Register your models here.
class CustomeUserAdmin(UserAdmin):
    
    add_form = RegisterForm  # the form to add user instance
    form = CustomeUserChangeForm # the form to chnage user instance
    
    model = CustomeUser
    
    # The fields to be used in displaying the User model
    # These override the def
    list_display = ('username','email', 'role', 'full_name','is_active',
                    'is_staff', 'is_superuser', 'last_login',)
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    
    fieldsets = (
        (None, {'fields': ('email','password' )}),
        ('Personal info', {'fields':('full_name', 'role')}),
                ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser','groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),

    )
    
    # add_fieldsets is not a standard ModelAdmain attribute. User Admin
    # overrides get_fieldsets to use this attribute when creating user.
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields': ('username','email', 'full_name','role', 'password1', 'password2') 
        }),
    )
    
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomeUser, CustomeUserAdmin)