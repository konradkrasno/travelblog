from django.views.generic import FormView

from .forms import CommentForm, SubCommentForm
from .mixins import CreateCommentMixin


class CreateCommentView(CreateCommentMixin, FormView):
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.commented_obj = self.object
        comment.save()
        return super().form_valid(form)


class CreateSubCommentView(CreateCommentMixin, FormView):
    form_class = SubCommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)
