from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, ListView, DetailView

from articles.models import Article
from common.decorators import ajax_required
from .forms import UserRegistrationForm, UserEditForm
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
    return render(request, "account/register.html", {"user_form": user_form, "section": "register"})


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
        following_ids = self.request.user.following.values_list("id", flat=True)
        if following_ids:
            articles = Article.pub_objects.filter(author_id__in=following_ids).order_by("-publish")[:10]
        else:
            articles = Article.pub_objects.all().order_by("-publish")[:10]
        data["articles"] = articles
        data["section"] = "dashboard"
        return data


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "account/list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data()
        data["section"] = "users"
        return data


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "account/detail.html"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data["articles"] = Article.pub_objects.filter(author=self.object)
        data["section"] = "users"
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
