from django.contrib import admin
from .models import ArticlePlace, Article


class ArticlePlaceInline(admin.TabularInline):
    model = ArticlePlace
    raw_id_fields = ["article"]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "author",
        "title",
        "slug",
        "body",
        "publish",
        "created",
        "updated",
        "published",
    ]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ArticlePlaceInline]
