from django import forms
from django.contrib.gis import forms as gis_forms
from django.utils.text import slugify

from .models import Place


class CreatePlaceForm(forms.ModelForm):
    location = gis_forms.PointField(
        widget=gis_forms.OSMWidget(attrs={"map_width": 600, "map_height": 500})
    )

    class Meta:
        model = Place
        fields = ["country", "city", "name"]

    def save(self, force_insert=False, force_update=False, commit=True):
        place = super().save(commit=False)
        place.slug = slugify(place.name)
        if commit:
            place.save()
        return place
