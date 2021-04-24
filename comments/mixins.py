from django.apps import apps
from django.http import HttpResponseForbidden
from django.views.generic.detail import SingleObjectMixin

from .forms import CommentForm, SubCommentForm
from .models import Comment


class CommentMixin(object):
    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data["comment_form"] = CommentForm()
        data["sub_comment_form"] = SubCommentForm()
        # data["comments"] = Comment.objects.filter(commented_obj=self.object)
        return data


class CreateCommentMixin(SingleObjectMixin):
    model = None

    def get_model(self, model_name):
        return apps.get_model(app_label=f"{model_name}s", model_name=model_name)

    def get_queryset(self):
        self.model = self.get_model(self.kwargs.get("model_name"))
        return super().get_queryset()

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return self.object.get_absolute_url()
