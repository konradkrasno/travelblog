from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Place


@admin.register(Place)
class PlaceAdmin(OSMGeoAdmin):
    list_display = [
        "author",
        "country",
        "city",
        "name",
        "slug",
        "location",
        "created",
    ]
    prepopulated_fields = {"slug": ("name",)}
