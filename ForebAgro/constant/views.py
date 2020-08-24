from django.shortcuts import render
from django.shortcuts import render, redirect,HttpResponseRedirect , get_object_or_404
from django.http import HttpResponse, request
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Constants, ConstantsForm
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
import datetime

# Create your views here.
@login_required
def add(request):
    if request.method == 'POST':
        form = ConstantsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/constants/constant_list')
    else:
        form = ConstantsForm()

    return render(request, "constant/constant_form.html", {"form": form, "messages": ''})

@login_required
def list(request):
    if 'constants_query' in request.GET:
        constants = Constants.objects.filter(constant_name__icontains=request.GET['constants_query'])
    else:
        constants = Constants.objects.all()[:20]

    return render(request, "constant/constant_list.html", {"constants": constants, "messages": ''})

@login_required
def update(request, id):
    if request.method == 'POST':
        pro = Constants.objects.get(id=id)
        form = ConstantsForm(request.POST, instance=pro)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.date_updated = datetime.datetime.now()
            obj.updated_by = request.user.get_username()
            form.save()
            return redirect('/constants/constant_list')
    else:

        pro = Constants.objects.get(id=id)
        form = ConstantsForm(instance=pro)

    return render(request, "constant/constant_update.html", {"form": form, "messages": ''})
