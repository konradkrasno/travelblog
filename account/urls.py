from django.urls import path

from . import views

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("users/", views.UserListView.as_view(), name="user_list"),
    path("users/<str:username>/", views.UserDetailView.as_view(), name="user_detail"),
    path("users/follow/", views.user_follow, name="user_follow"),
]
