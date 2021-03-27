from django.contrib import admin

from .models import Article, ArticlePlace, ArticleComment, SubComment


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


@admin.register(ArticleComment)
class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = [
        "article",
        "author",
        "body",
        "created",
        "updated",
        "active",
    ]
    list_editable = ["active"]


@admin.register(SubComment)
class SubCommentAdmin(admin.ModelAdmin):
    list_display = [
        "main_comment",
        "author",
        "body",
        "created",
        "updated",
        "active",
    ]
    list_editable = ["active"]
