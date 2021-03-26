from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from common.decorators import ajax_required
from django.views.decorators.http import require_POST

from .models import User, Follow


def register(request):
    pass


def edit(request):
    pass


class DashboardView(TemplateView):
    template_name = "account/dashboard.html"


class UserListView(ListView):
    model = User
    template_name = "account/list.html"


class UserDetailView(DetailView):
    model = User
    template_name = "account/detail.html"
    slug_field = "username"
    slug_url_kwarg = "username"


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
                Contact.objects.filter(
                    user_from=request.user,
                    user_to=user,
                ).delete()
            return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"})
