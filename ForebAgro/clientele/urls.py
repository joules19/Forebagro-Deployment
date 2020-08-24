from django.conf.urls import url
from . import views

app_name = 'clientele'

urlpatterns = [
                url(r'^clientele/$', views.clientele, name='clientele_list'),
                url(r'^debtor/$', views.debtor, name='clientele_debtor'),
                url(r'^creditor/$', views.creditor, name='clientele_creditor'),
                url(r'^register/$', views.register, name='register_clientele'),
                url(r'^update_clientele/(?P<id>\d+)/$', views.clientele_update, name='update'),
                url(r'^delete_clientele/(?P<pk>\d+)/$', views.ClienteleDeleteView.as_view(), name='delete'),
                #url(r'^id/([0-9]+)/order/add/$', views.add_order, name='add_order'),
                #url(r'^order/save/$', views.save_order, name='save_order'),
                url(r'^csv/$', views.getfile, name='get'),

 ]