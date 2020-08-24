from django.shortcuts import render, redirect,HttpResponseRedirect , get_object_or_404
from django.http import HttpResponse, request
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, ProductForm
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

# Create your views here.
@login_required
def add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/products/product_list')
    else:
        form = ProductForm()

    return render(request, "products/product_form.html", {"form": form, "messages": ''})

@login_required
def list(request):
    if 'products_query' in request.GET:
        products = Product.objects.filter(product_name__icontains=request.GET['products_query'])
    else:
        products = Product.objects.all()[:20]

    return render(request, "products/product_list.html", {"products": products, "messages": ''})

@login_required
def update(request, id):
    if request.method == 'POST':
        pro = Product.objects.get(id=id)
        form = ProductForm(request.POST, instance=pro)
        if form.is_valid():
            form.save()
            return redirect('/products/product_list')
    else:

        pro = Product.objects.get(id=id)
        form = ProductForm(instance=pro)

    return render(request, "products/product_update.html", {"form": form, "messages": ''})

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('products:list')
