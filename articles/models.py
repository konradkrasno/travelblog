from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

from account.models import User
from places.models import Place


class ArticleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(publish=True)


class Article(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="articles", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    body = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=False)
    objects = models.Manager()
    pub_objects = ArticleManager()
    places = models.ManyToManyField(
        Place, through="ArticlePlace", related_name="articles"
    )

    class Meta:
        ordering = ("-published",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("articles:detail", args=[self.id, self.slug])


class ArticlePlace(models.Model):
    article = models.ForeignKey(
        Article, related_name="article_places", on_delete=models.CASCADE
    )
    place = models.ForeignKey(
        Place, related_name="article_places", on_delete=models.CASCADE
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.article}:{self.place}"


class CommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class ArticleComment(models.Model):
    article = models.ForeignKey(
        Article, related_name="comments", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User, related_name="article_comments", on_delete=models.CASCADE
    )
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    objects = CommentManager()

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.article.title}"


class SubComment(models.Model):
    main_comment = models.ForeignKey(
        ArticleComment, related_name="sub_comments", on_delete=models.CASCADE, null=True
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
