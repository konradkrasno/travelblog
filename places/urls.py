from django.urls import path
from django.views.decorators.http import require_POST

from . import views

app_name = "places"

urlpatterns = [
    path("add_image/<int:pk>/", require_POST(views.AddImageView.as_view()), name="add_image"),
    path("create/", views.CreatePlaceView.as_view(), name="create"),
    path(
        "update/<int:pk>/<slug:slug>/", views.UpdatePlaceView.as_view(), name="update"
    ),
    path("delete/<int:pk>/", views.DeletePlaceView.as_view(), name="delete"),
    path("<str:username>/data.geojson", views.MapLayer.as_view(), name="data"),
    path("list/<str:username>/", views.PlaceListView.as_view(), name="list"),
    path("<int:pk>/<slug:slug>/", views.PlaceDetailView.as_view(), name="detail"),
]
