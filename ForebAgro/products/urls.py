from django.conf.urls import url, include, url
from products import views

urlpatterns = [
    url(r'^add_product/$', views.add, name='add'),
    url(r'^product_list/$', views.list, name='list'),
    url(r'^update/(?P<id>\d+)/$', views.update, name='update'),
    url(r'^delete_product/(?P<pk>\d+)/$', views.ProductDeleteView.as_view(), name='delete'),

]