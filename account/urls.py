from django.urls import path, include

from . import views

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("register", views.register, name="register"),
    path("edit", views.edit, name="edit"),
    path("users/", views.UserListView.as_view(), name="user_list"),
    path("users/<str:username>/", views.UserDetailView.as_view(), name="user_detail"),
    path("follow/", views.user_follow, name="user_follow"),
]
