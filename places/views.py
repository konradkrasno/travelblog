from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.shortcuts import render_to_kml
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from djgeojson.views import GeoJSONLayerView

from .forms import ImagesFormSet, PlaceForm
from .models import Place


class PlaceListView(LoginRequiredMixin, ListView):
    model = Place
    template_name = "places/place/list.html"

    def get_queryset(self):
        username = self.kwargs.get("username", self.request.user.username)
        return super().get_queryset().filter(author__username=username)


class PlaceDetailView(LoginRequiredMixin, DeleteView):
    model = Place
    template_name = "places/place/detail.html"


class CreatePlaceView(LoginRequiredMixin, CreateView):
    model = Place
    template_name = "places/place/place_form.html"
    form_class = PlaceForm
    template_title = "Create Place"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = self.template_title
        if self.request.POST:
            data["images_form"] = ImagesFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            data["images_form"] = ImagesFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        images_form = context["images_form"]
        if not images_form.is_valid():
            return super().form_invalid(form)
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.location = form.cleaned_data["location"]
        self.object.save()
        if images_form.is_valid():
            images_form.instance = self.object
            images = images_form.save(commit=False)
            for image in images:
                image.author = self.request.user
                image.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("places:list", args=[self.request.user.username])


class UpdatePlaceView(CreatePlaceView, UpdateView):
    template_title = "Update Place"

    def get_success_url(self):
        return self.object.get_absolute_url()


class DeletePlaceView(LoginRequiredMixin, DeleteView):
    model = Place
    template_name = "confirm_delete.html"

    def get_success_url(self):
        return reverse("places:list", args=[self.request.user.username])


class MapLayer(LoginRequiredMixin, GeoJSONLayerView):
    model = Place
    geometry_field = "location"

    def get_queryset(self):
        username = self.kwargs.get("username", self.request.user.username)
        return super().get_queryset().filter(author__username=username)
