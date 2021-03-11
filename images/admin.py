from django.contrib import admin
from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["author", "title", "slug", "image", "place"]
    prepopulated_fields = {"slug": ("title",)}
