from django.contrib import admin

from .models import Article, ArticlePlace


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
        "published",
        "created",
        "updated",
        "publish",
    ]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ArticlePlaceInline]
