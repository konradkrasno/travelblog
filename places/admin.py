from django.contrib import admin
from .models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = [
        "country",
        "locality",
        "name",
        "slug",
        "latitude",
        "longitude",
        "images",
    ]
    prepopulated_fields = {"slug": ("name",)}
