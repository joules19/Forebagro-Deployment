from django.shortcuts import render, redirect,HttpResponseRedirect , get_object_or_404
from django.views.generic import TemplateView
from .models import Contact, ContactForm
from django.contrib import messages

# Create your views here.
def send(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message Sent')
            return redirect('/contact-us')
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form, "messages": 'messages'})
