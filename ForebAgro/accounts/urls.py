from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views


app_name = 'accounts'

urlpatterns = [

    url(r"^$", auth_views.login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r"logout/$", auth_views.logout, name="logout"),
    url(r'^add_new_user/$', views.add_new_user, name='add_new_user'),
    url(r'^register/$', views.register, name='register'),
    url(r'^list/$', views.user_list, name='user_list'),
    #url(r'^delete_user/(?P<pk>\d+)/$', views.UserDeleteView.as_view(), name='delete'),
    url(r'^password-change/(?P<id>\d+)/$', views.password_change, name='password_change'),
    #url(r'^password_change/done/(?P<id>\d+)/$', views.change_password, name='password_change_done'),


]