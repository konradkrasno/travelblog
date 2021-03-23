from django.urls import path

from . import views

app_name = "articles"

urlpatterns = [
    path("create/", views.CreateArticleView.as_view(), name="create"),
    path("update/<int:pk>/<slug:slug>/", views.UpdateArticleView.as_view(), name="update"),
    path("delete/<int:pk>/", views.DeleteArticleView.as_view(), name="delete"),
    path("dashboard/", views.ArticleListView.as_view(), name="dashboard"),
    path("list/<str:username>/", views.ArticleListView.as_view(), name="list"),
    path(
        "<int:pk>/<slug:slug>/",
        views.ArticleDetailView.as_view(),
        name="detail",
    ),
]
