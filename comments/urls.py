from django.urls import path
from django.views.decorators.http import require_POST

from . import views

app_name = "comments"

urlpatterns = [
    path(
        "comment/<model_name>/<int:pk>/",
        require_POST(views.CreateCommentView.as_view()),
        name="create_comment",
    ),
    path(
        "sub_comment/<model_name>/<int:pk>/",
        require_POST(views.CreateSubCommentView.as_view()),
        name="create_sub_comment",
    ),
]
