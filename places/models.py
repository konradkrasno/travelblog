from django.conf import settings
from django.contrib.gis.db import models
from django.urls import reverse


class Place(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="places", on_delete=models.CASCADE
    )
    country = models.CharField(max_length=100, db_index=True)
    city = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    location = models.PointField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("places:detail", args=[self.id, self.slug])
