from django import forms
from django.utils.text import slugify
from django.core.files.base import ContentFile

from .models import Image


class AddImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["title", "image"]

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False)
        image.slug = slugify(image.title)
        if commit:
            image.save()
        return image
