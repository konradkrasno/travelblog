from django.conf import settings
from django.db import models
from django.urls import reverse
from places.models import Place


class Image(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="images", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    image = models.ImageField(upload_to="images/%Y/%m/%d")
    created = models.DateTimeField(auto_now_add=True)
    place = models.ForeignKey(
        Place, related_name="images", on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("images:detail", args=[self.id, self.slug])
