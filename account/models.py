from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    following = models.ManyToManyField(
        "self", through="Follow", related_name="followers", symmetrical=False
    )

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
