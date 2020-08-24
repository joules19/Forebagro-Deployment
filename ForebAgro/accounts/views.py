from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, CreateView
from . import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import update_session_auth_hash
from accounts.models import User
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
from django.contrib.auth import get_user_model


def add_new_user(request):
    form = forms.UserCreateForm
    return render(request, "user_register.html", {"form": form})


def user_list(request):
    # Users = User.objects.all()
    users = get_user_model().objects.order_by("id")
    return render(request, "user_list.html", {"user_list": users})

def register(request):
    if request.method == "POST":
        form = forms.UserCreateForm(data=request.POST)

        if form.is_valid():
            form.save()
            return render(request, "userreg_successful.html")
        else:
            pass
    else:
        form = forms.UserCreateForm()

    return render(request, 'user_register.html', {'form': form})

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('accounts:user_list')


def password_change(request, id):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return render(request, "change_successful.html")
        else:
            print(form.errors)

    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'change_password.html', {'form': form})
