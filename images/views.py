from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView

from comments.mixins import CommentMixin
from common.mixins import DisplayCounterMixin
from places.models import Place
from .forms import AddImageForm
from .models import Image


class ImageListView(LoginRequiredMixin, ListView):
    model = Image
    template_name = "images/image/list.html"

    def get_queryset(self):
        username = self.kwargs.get("username", self.request.user.username)
        return super().get_queryset().filter(author__username=username)


class ImageDetailView(
    LoginRequiredMixin, DisplayCounterMixin, CommentMixin, DetailView
):
    model = Image
    template_name = "images/image/detail.html"


class AddImageView(LoginRequiredMixin, CreateView):
    model = Image
    template_name = "images/image/create.html"
    form_class = AddImageForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        place_id = self.kwargs.get("place_id")
        place = get_object_or_404(Place, id=place_id)
        data["place"] = place
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        place = context["place"]
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.place = place
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class DeleteImageView(LoginRequiredMixin, DeleteView):
    model = Image
    template_name = "confirm_delete.html"

    def get_success_url(self):
        return self.object.place.get_absolute_url()
