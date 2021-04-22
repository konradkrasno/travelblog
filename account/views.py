from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, ListView, DetailView

from articles.forms import ArticleSearchForm
from articles.models import Article
from common.decorators import ajax_required
from places.forms import PlaceSearchForm
from places.models import Place
from .forms import UserRegistrationForm, UserEditForm, UserSearchForm
from .models import User, Follow


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            return render(request, "account/register_done.html", {"new_user": new_user})
    user_form = UserRegistrationForm()
    return render(
        request,
        "account/register.html",
        {"user_form": user_form, "section": "register"},
    )


def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Profile updated successfully")
        else:
            messages.error(request, "Error updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, "account/edit.html", {"user_form": user_form})


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "account/dashboard.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        articles = None
        places = None
        if "place_search" in self.request.GET:
            place_search = self.request.GET["place_search"]
            places = Place.objects.search_by_name(place_search)
        elif "article_search" in self.request.GET:
            article_search = self.request.GET["article_search"]
            articles = Article.pub_objects.search_by_title(article_search)
        else:
            following_ids = self.request.user.following.values_list("id", flat=True)
            if following_ids:
                articles = Article.pub_objects.filter(
                    author_id__in=following_ids
                ).order_by("-publish")[:10]
            else:
                articles = Article.pub_objects.all().order_by("-publish")[:10]
        data["articles"] = articles
        data["places"] = places
        data["section"] = "dashboard"
        data["article_search_form"] = ArticleSearchForm()
        data["place_search_form"] = PlaceSearchForm()
        return data


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "account/list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data()
        data["user_search_form"] = UserSearchForm()
        data["section"] = "users"
        return data

    def get_queryset(self):
        if "user_search" in self.request.GET:
            user_search = self.request.GET["user_search"]
            return User.objects.search_by_username(user_search)
        return super().get_queryset()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "account/detail.html"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data["article_search_form"] = ArticleSearchForm()
        data["place_search_form"] = PlaceSearchForm()
        data["section"] = "users"
        articles = None
        places = None
        if "place_search" in self.request.GET:
            place_search = self.request.GET["place_search"]
            places = Place.objects.search_by_name(place_search).filter(
                author=self.object
            )
        elif "article_search" in self.request.GET:
            article_search = self.request.GET["article_search"]
            articles = Article.pub_objects.search_by_title(article_search, articles)
        else:
            articles = Article.pub_objects.filter(author=self.object)
        data["articles"] = articles
        data["places"] = places
        return data


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get("id")
    action = request.POST.get("action")
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"status": "error"})
        else:
            if action == "follow":
                Follow.objects.get_or_create(
                    user_from=request.user,
                    user_to=user,
                )
            else:
                Follow.objects.filter(
                    user_from=request.user,
                    user_to=user,
                ).delete()
            return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"})
