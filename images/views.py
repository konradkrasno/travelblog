from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

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
def add_image(request):
    if request.method == "POST":
        form = AddImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.author = request.user
            image.save()
            return render(request, "images/image/detail.html", {"image": image})
    else:
        form = AddImageForm()
    return render(request, "images/image/create.html", {"form": form})


@login_required
def remove_image(request):
    pass
