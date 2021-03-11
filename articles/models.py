from django.conf import settings
from django.db import models
from django.utils import timezone
from places.models import Place


class Article(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="articles", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ("-publish",)

    def __str__(self):
        return f"<Article: {self.title}>"


class ArticlePlace(models.Model):
    article = models.ForeignKey(
        Article, related_name="article_places", on_delete=models.CASCADE, blank=True
    )
    place = models.ForeignKey(
        Place, related_name="article_place", on_delete=models.CASCADE
    )
    description = models.TextField()
