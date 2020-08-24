from django.shortcuts import render, redirect,HttpResponseRedirect , get_object_or_404
from django.views.generic import TemplateView
from contact.models import Contact, ContactForm

def ContactPage(request):
    form = ContactForm()
    return render(request, "contact.html", {"form": form, "messages": ''})


class AboutPage(TemplateView):
    template_name = 'about_us.html'

class HomePage(TemplateView):
    template_name = "index.html"
