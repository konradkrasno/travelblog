from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from account.models import User


class CommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class Comment(models.Model):
    author = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    objects = CommentManager()
    commented_obj_ct = models.ForeignKey(
        ContentType, related_name="comments", on_delete=models.CASCADE
    )
    commented_obj_id = models.PositiveIntegerField()
    commented_obj = GenericForeignKey("commented_obj_ct", "commented_obj_id")

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.commented_obj}"


class SubComment(models.Model):
    main_comment = models.ForeignKey(
        Comment, related_name="sub_comments", on_delete=models.CASCADE, null=True
    )
    author = models.ForeignKey(
        User, related_name="sub_comments", on_delete=models.CASCADE
    )
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    objects = CommentManager()

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.main_comment.author.username} comment"
