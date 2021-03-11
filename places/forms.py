from django import forms
from django.utils.text import slugify

from .models import Place


class CreatePlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ["name"]
    
    def save(self, force_insert=False, force_update=False, commit=True):
        place = super().save(commit=False)
        place.slug = slugify(place.name)

        # TODO download data from google maps

        if commit:
            place.save()
        return place
