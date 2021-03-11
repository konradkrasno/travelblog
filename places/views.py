from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

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
    # TODO finish
    # TODO consider google maps api
    return render(request, "places/place/create.html")


@login_required
def remove_place(request):
    pass
