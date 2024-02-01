from django.contrib import admin
from .models import Booking

# Register your models here.


class BookingAdmin(admin.ModelAdmin):
    list_display = ["player", "slot", "status"]
    list_filter = ["player", "status"]


admin.site.register(Booking, BookingAdmin)
