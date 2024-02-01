from django.contrib import admin
from .models import Slot


# Register your models here.
class SlotAdmin(admin.ModelAdmin):
    list_display = ["day", "start_hour", "end_hour", "playground", "price", "status"]
    list_filter = [
        "status",
        "playground",
        "day",
        "start_hour",
        "end_hour",
    ]
    search_fields = ["playground"]


admin.site.register(Slot, SlotAdmin)
