from django.conf.urls import url
from . import views

app_name = 'transactions'

urlpatterns = [
                url(r'^record_expense/$', views.record, name='record_expense'),
                url(r'^customer_debt/$', views.customer, name='customer_debt'),
                url(r'^foreb_debt/$', views.foreb, name='foreb_debt'),
                url(r'^purchase/$', views.purchase, name='purchase'),
                url(r'^sales/$', views.sales, name='sales'),

                url(r'^customer_transactions/$', views.showcustomer, name='show_customer'),
                url(r'^foreb_transactions/$', views.showforeb, name='show_foreb'),
                url(r'^sales_transactions/$', views.showsales, name='show_sales'),
                url(r'^purchase_transactions/$', views.showpurchase, name='show_purchase'),
                url(r'^expense_transactions/$', views.showexpense, name='show_expense'),

                url(r'^customer-transactions/$', views.showcustomer_user, name='show_customer_user'),
                url(r'^foreb-transactions/$', views.showforeb_user, name='show_foreb_user'),
                url(r'^sales-transactions/$', views.showsales_user, name='show_sales_user'),
                url(r'^purchase-transactions/$', views.showpurchase_user, name='show_purchase_user'),
                url(r'^expense-transactions/$', views.showexpense_user, name='show_expense_user'),

                url(r'^sales_details/(?P<id>\d+)/$', views.sales_details, name='sales_details'),
                url(r'^purchase_details/(?P<id>\d+)/$', views.purchase_details, name='purchase_details'),
                url(r'^foreb_details/(?P<id>\d+)/$', views.foreb_details, name='foreb_details'),
                url(r'^customer_details/(?P<id>\d+)/$', views.customer_details, name='customer_details'),
                url(r'^expense_details/(?P<id>\d+)/$', views.expense_details, name='expense_details'),

                url(r'^approve_sales/(?P<id>\d+)/$', views.sales_approve, name='approve_sales'),
                url(r'^approve_purchase/(?P<id>\d+)/$', views.purchase_approve, name='approve_purchase'),
                url(r'^approve_foreb/(?P<id>\d+)/$', views.foreb_approve, name='approve_foreb'),
                url(r'^approve_customer/(?P<id>\d+)/$', views.customer_approve, name='approve_customer'),
                url(r'^approve_expense/(?P<id>\d+)/$', views.expense_approve, name='approve_expense'),

                url(r'^view-summary/$', views.view_summary, name='view_summary'),
                url(r'^summary/$', views.summary, name='summary'),
                url(r'^view-customer-statement/$', views.view_customer_statement, name='view_customer_statement'),
                url(r'^customer-statement/$', views.customer_statement, name='customer_statement'),

                url(r'^update-sales/(?P<id>\d+)/$', views.update_sales, name='update_sales'),
                url(r'^update-expense/(?P<id>\d+)/$', views.update_expense, name='update_expense'),
                url(r'^update-purchase/(?P<id>\d+)/$', views.update_purchase, name='update_purchase'),
                url(r'^update-customer/(?P<id>\d+)/$', views.update_customer, name='update_customer'),
                url(r'^update-foreb/(?P<id>\d+)/$', views.update_foreb, name='update_foreb'),

                url(r'^delete-sales/(?P<pk>\d+)/$', views.SalesDeleteView.as_view(), name='delete_sales'),
                url(r'^delete-purchase/(?P<pk>\d+)/$', views.PurchaseDeleteView.as_view(), name='delete_purchase'),
                url(r'^delete-expense/(?P<pk>\d+)/$', views.ExpenseDeleteView.as_view(), name='delete_expense'),
                url(r'^delete-foreb/(?P<pk>\d+)/$', views.ForebDeleteView.as_view(), name='delete_foreb'),
                url(r'^delete-customer/(?P<pk>\d+)/$', views.CustomerDeleteView.as_view(), name='delete_customer'),

                url(r'^homepage/$', views.HomePage.as_view(), name="home"),
]
