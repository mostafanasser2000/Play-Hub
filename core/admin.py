from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Playground


class PlaygroundAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
        "city",
        "capacity",
        "grass_type",
        "image",
        "owner",
    ]
    list_filter = ["city", "capacity", "grass_type", "owner"]
    search_fields = ["name", "city"]
    ordering = ["name", "city"]
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ()


admin.site.register(Playground, PlaygroundAdmin)
