from django.conf.urls import url, include, url
from constant import views

urlpatterns = [
    url(r'^add_constant/$', views.add, name='add'),
    url(r'^constant_list/$', views.list, name='list'),
    url(r'^update/(?P<id>\d+)/$', views.update, name='update'),
]