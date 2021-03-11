from django.urls import path

from . import views

app_name = "images"

urlpatterns = [
    path("", views.image_list, name="list"),
    path("<int:image_id>/<slug:slug>/", views.image_detail, name="detail"),
    path("add/", views.add_image, name="add"),
    path("remove/", views.remove_image, name="remove"),
]
