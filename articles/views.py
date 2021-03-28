from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import (
    ArticleForm,
    ArticlePlacesFormSet,
    ArticleCommentForm,
    SubCommentForm,
    ArticleSearchForm,
)
from .models import Article


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "articles/article/list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data()
        data["article_search_form"] = ArticleSearchForm()
        return data

    def get_queryset(self):
        username = self.kwargs.get("username")
        if username:
            articles = Article.pub_objects.filter(author__username=username)
        else:
            articles = self.request.user.articles.all()
        if "article_search" in self.request.GET:
            article_search = self.request.GET["article_search"]
            articles = Article.pub_objects.search_by_title(article_search, objects=articles)
        return articles


class ArticleDisplayView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = "articles/article/detail.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data["comment_form"] = ArticleCommentForm()
        data["sub_comment_form"] = SubCommentForm()
        return data


class ArticleCommentView(SingleObjectMixin, FormView):
    model = Article
    template_name = "articles/article/detail.html"
    form_class = ArticleCommentForm

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.article = self.object
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class ArticleSubCommentView(SingleObjectMixin, FormView):
    model = Article
    template_name = "articles/article/detail.html"
    form_class = SubCommentForm

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class ArticleDetailView(View):
    def get(self, request, *args, **kwargs):
        view = ArticleDisplayView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if "main_comment" in request.POST:
            view = ArticleSubCommentView.as_view()
        else:
            view = ArticleCommentView.as_view()
        return view(request, *args, **kwargs)


class CreateArticleView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "articles/article/article_form.html"
    form_class = ArticleForm
    template_title = "Create Article"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = self.template_title
        if self.request.POST:
            data["article_places"] = ArticlePlacesFormSet(
                self.request.POST, instance=self.object, user=self.request.user
            )
        else:
            data["article_places"] = ArticlePlacesFormSet(
                instance=self.object, user=self.request.user
            )
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        article_places = context["article_places"]
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        if article_places.is_valid():
            article_places.instance = self.object
            article_places.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("articles:dashboard")


class UpdateArticleView(CreateArticleView, UpdateView):
    template_title = "Update Article"

    def get_success_url(self):
        return self.object.get_absolute_url()


class DeleteArticleView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = "confirm_delete.html"

    def get_success_url(self):
        return reverse("articles:dashboard")
