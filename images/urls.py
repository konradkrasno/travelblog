from django.urls import path

from . import views

app_name = "images"

urlpatterns = [
    path("add/<int:place_id>/", views.AddImageView.as_view(), name="add"),
    path("delete/<int:pk>/", views.DeleteImageView.as_view(), name="delete"),
    path("list/<str:username>/", views.ImageListView.as_view(), name="list"),
    path("<int:pk>/<slug:slug>/", views.ImageDetailView.as_view(), name="detail"),
]
