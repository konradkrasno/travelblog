from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.shortcuts import render_to_kml
from django.shortcuts import get_object_or_404, redirect, render
from djgeojson.views import GeoJSONLayerView

from .forms import CreatePlaceForm
from .models import Place


@login_required
def place_list(request):
    places = request.user.places.all()
    return render(request, "places/place/list.html", {"places": places})


@login_required
def place_detail(request, place_id: int, slug: str):
    place = get_object_or_404(Place, id=place_id, slug=slug)
    return render(request, "places/place/detail.html", {"place": place})


@login_required
def add_place(request):
    if request.method == "POST":
        form = CreatePlaceForm(request.POST)
        if form.is_valid():
            place = form.save(commit=False)
            place.author = request.user
            place.location = form.cleaned_data["location"]
            place.save()
            return redirect("places:detail", place_id=place.id, slug=place.slug)
    else:
        form = CreatePlaceForm()
    return render(request, "places/place/create.html", {"form": form})


@login_required
def remove_place(request, place_id: int):
    Place.objects.filter(id=place_id).delete()
    return redirect("places:list")


class MapLayer(LoginRequiredMixin, GeoJSONLayerView):
    model = Place
    geometry_field = "location"

    def get_queryset(self):
        return self.request.user.places.all()
