from django.contrib import admin

from .models import Comment, SubComment


@admin.register(Comment)
class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = [
        "commented_obj",
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
