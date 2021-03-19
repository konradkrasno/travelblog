from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from places.models import Place

from .forms import AddImageForm
from .models import Image


@login_required
def image_list(request):
    images = request.user.images.all()
    return render(request, "images/image/list.html", {"images": images})


@login_required
def image_detail(request, image_id: int, slug: str):
    image = get_object_or_404(Image, id=image_id, slug=slug)
    return render(request, "images/image/detail.html", {"image": image})


@login_required
def add_image(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    if request.method == "POST":
        form = AddImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.author = request.user
            image.place = place
            image.save()
            return redirect("places:detail", place_id=image.place.id, slug=image.place.slug)
    else:
        form = AddImageForm()
    return render(request, "images/image/create.html", {"form": form})


@login_required
def remove_image(request):
    pass
