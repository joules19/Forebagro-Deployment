from django.conf.urls import url, include, url
from contact import views

urlpatterns = [
    url(r'^contact-us/$', views.send, name='send'),
]