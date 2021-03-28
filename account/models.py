from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db import models
from django.urls import reverse


class CustomUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset()

    def search_by_username(self, search_text):
        vector = SearchVector("username")
        query = SearchQuery(search_text)
        return (
            self.get_queryset()
            .annotate(search=vector, rank=SearchRank(vector, query))
            .filter(search=search_text)
            .order_by("-rank")
        )


class User(AbstractUser):
    following = models.ManyToManyField(
        "self", through="Follow", related_name="followers", symmetrical=False
    )
    objects = CustomUserManager()

    def get_absolute_url(self):
        return reverse("user_detail", args=[self.username])


class Follow(models.Model):
    user_from = models.ForeignKey(
        User, related_name="rel_from_set", on_delete=models.CASCADE
    )
    user_to = models.ForeignKey(
        User, related_name="rel_to_set", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"
