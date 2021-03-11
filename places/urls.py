from django.urls import path

from . import views

app_name = "places"

urlpatterns = [
    path("", views.place_list, name="list"),
    path("<int:place_id>/<slug:slug>/", views.place_detail, name="detail"),
    path("add", views.add_place, name="add"),
    path("remove", views.remove_place, name="remove"),
]
