from django import forms
from django.contrib.gis import forms as gis_forms
from django.forms.models import inlineformset_factory
from django.utils.text import slugify
from images.forms import AddImageForm
from images.models import Image

from .models import Place


class PlaceForm(forms.ModelForm):
    location = gis_forms.PointField(
        widget=gis_forms.OSMWidget(
            attrs={
                "map_width": 700,
                "map_height": 500,
                "default_lon": 21.0123297,
                "default_lat": 52.2315696,
                "default_zoom": 1,
            }
        )
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


ImagesFormSet = inlineformset_factory(Place, Image, form=AddImageForm, can_delete=False)


class PlaceSearchForm(forms.Form):
    place_search = forms.CharField(label="Search", help_text="Search for places")
