from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, request
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import csv
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Clientele, ClienteleForm
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
from transactions.models import TransactionRecord
from django.core import serializers

# Create your views here.
@login_required
def clientele(request):
    clientele = Clientele.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(clientele, 10)
    try:
        clienteles = paginator.page(page)
    except PageNotAnInteger:
        clienteles = paginator.page(1)
    except EmptyPage:
        clienteles = paginator.page(paginator.num_pages)
    return render(request, 'clientele/clientele_list.html', { 'clienteles': clienteles })


@login_required
def creditor(request):
    d_name = []
    c_name = []
    ids = Clientele.objects.filter().values_list('id', flat=True)
    debtoroutstandingList = []
    creditoroutstandingList = []
    for d in ids:
        qj = TransactionRecord.objects.raw(
            "Select 1 as id, SUM(OUTSTANDING) as outstanding FROM (Select 0 AS TRANSACTION_COST, sales.transaction_income AS INCOME, sales.amount_paid AS AMOUNT_PAID, (sales.amount_paid-sales.transaction_income) AS OUTSTANDING, CASE WHEN (sales.transaction_income-sales.amount_paid) >= 0 " +
            "THEN 'DEBIT' ELSE 'CREDIT'  END AS LEG_TYPE from transactions_record Tr Left join clientele client On Tr.clientele_id= client.id Left Join sales_transactions sales ON Tr.transaction_reference= sales.transaction_reference Where Tr.clientele_id = %s " +
            "and Tr.transaction_status='approved' " +
            "UNION " +
            "Select  PT.transaction_cost AS COST, 0 AS TRANSACTION_INCOME,PT.amount_paid AS AMOUNT_PAID,(PT.transaction_cost-PT.amount_paid) AS OUTSTANDING, CASE WHEN (PT.transaction_cost-PT.amount_paid) >= 0 THEN 'CREDIT' ELSE 'DEBIT'  END AS LEG_TYPE " +
            "from transactions_record Tr Left join clientele client On Tr.clientele_id= client.id Left Join purchase_transactions PT ON Tr.transaction_reference= PT.transaction_reference Where Tr.clientele_id = %s and Tr.transaction_status='approved' " +
            "UNION " +
            "Select  CDT.amount_paid AS COST, 0 AS TRANSACTION_INCOME,CDT.amount_paid AS AMOUNT_PAID,(CDT.amount_paid) AS OUTSTANDING, 'CREDIT' AS LEG_TYPE from transactions_record Tr Left join clientele client On Tr.clientele_id= client.id " +
            "Left Join customer_debt_transactions CDT ON Tr.transaction_reference= CDT.transaction_reference Where Tr.clientele_id = %s  and Tr.transaction_status='approved' " +
            "UNION " +
            "Select  0 AS COST, FDT.amount_paid AS TRANSACTION_INCOME,FDT.amount_paid AS AMOUNT_PAID,(FDT.amount_paid * -1) AS OUTSTANDING, 'DEBIT' AS LEG_TYPE from transactions_record Tr	Left join clientele client " +
            "On Tr.clientele_id= client.id Left Join foreb_debt_transactions FDT ON Tr.transaction_reference= FDT.transaction_reference Where Tr.clientele_id = %s  and Tr.transaction_status='approved')",
            [d, d, d, d])
        customer_names = Clientele.objects.filter(pk=d).values()[0]
        customer_name = customer_names["clientele_name"]

        qjj = list(qj)
        J = []
        for q in qjj:
            if q.outstanding is None:
                J.append(0)
            else:
                J.append(q.outstanding)

            for i in J:
                if i < 0:
                    d_name.append(customer_name)
                    debtoroutstandingList.append(i)
                else:
                    c_name.append(customer_name)
                    creditoroutstandingList.append(i)

    debtors = dict(zip(d_name, debtoroutstandingList))
    creditors = dict(zip(c_name, creditoroutstandingList))
    new_creditor = creditors.items()
    creditor_r = list(new_creditor)

    page = request.GET.get('page', 1)

    paginator = Paginator(creditor_r, 10)
    try:
        creditor = paginator.page(page)
    except PageNotAnInteger:
        creditor = paginator.page(1)
    except EmptyPage:
        creditor = paginator.page(paginator.num_pages)
    print(creditor)
    return render(request, "clientele/creditors.html", {'creditor': creditor})


@login_required
def debtor(request):
    d_name = []
    c_name = []
    ids = Clientele.objects.filter().values_list('id', flat=True)
    debtoroutstandingList = []
    creditoroutstandingList = []
    for d in ids:
        qj = TransactionRecord.objects.raw(
            "Select 1 as id, SUM(OUTSTANDING) as outstanding FROM (Select 0 AS TRANSACTION_COST, sales.transaction_income AS INCOME, sales.amount_paid AS AMOUNT_PAID, (sales.amount_paid-sales.transaction_income) AS OUTSTANDING, CASE WHEN (sales.transaction_income-sales.amount_paid) >= 0 " +
            "THEN 'DEBIT' ELSE 'CREDIT'  END AS LEG_TYPE from transactions_record Tr Left join clientele client On Tr.clientele_id= client.id Left Join sales_transactions sales ON Tr.transaction_reference= sales.transaction_reference Where Tr.clientele_id = %s " +
            "and Tr.transaction_status='approved' " +
            "UNION " +
            "Select  PT.transaction_cost AS COST, 0 AS TRANSACTION_INCOME,PT.amount_paid AS AMOUNT_PAID,(PT.transaction_cost-PT.amount_paid) AS OUTSTANDING, CASE WHEN (PT.transaction_cost-PT.amount_paid) >= 0 THEN 'CREDIT' ELSE 'DEBIT'  END AS LEG_TYPE " +
            "from transactions_record Tr Left join clientele client On Tr.clientele_id= client.id Left Join purchase_transactions PT ON Tr.transaction_reference= PT.transaction_reference Where Tr.clientele_id = %s and Tr.transaction_status='approved' " +
            "UNION " +
            "Select  CDT.amount_paid AS COST, 0 AS TRANSACTION_INCOME,CDT.amount_paid AS AMOUNT_PAID,(CDT.amount_paid) AS OUTSTANDING, 'CREDIT' AS LEG_TYPE from transactions_record Tr Left join clientele client On Tr.clientele_id= client.id " +
            "Left Join customer_debt_transactions CDT ON Tr.transaction_reference= CDT.transaction_reference Where Tr.clientele_id = %s  and Tr.transaction_status='approved' " +
            "UNION " +
            "Select  0 AS COST, FDT.amount_paid AS TRANSACTION_INCOME,FDT.amount_paid AS AMOUNT_PAID,(FDT.amount_paid * -1) AS OUTSTANDING, 'DEBIT' AS LEG_TYPE from transactions_record Tr	Left join clientele client " +
            "On Tr.clientele_id= client.id Left Join foreb_debt_transactions FDT ON Tr.transaction_reference= FDT.transaction_reference Where Tr.clientele_id = %s  and Tr.transaction_status='approved')",
            [d, d, d, d])
        customer_names = Clientele.objects.filter(pk=d).values()[0]
        customer_name = customer_names["clientele_name"]

        qjj = list(qj)
        J = []
        for q in qjj:
            if q.outstanding is None:
                J.append(0)
            else:
                J.append(q.outstanding)

            for i in J:
                if i < 0:
                    d_name.append(customer_name)
                    debtoroutstandingList.append(i)
                else:
                    c_name.append(customer_name)
                    creditoroutstandingList.append(i)

    debtors = dict(zip(d_name, debtoroutstandingList))
    creditors = dict(zip(c_name, creditoroutstandingList))
    new_debtor = debtors.items()
    debtor_r = list(new_debtor)

    page = request.GET.get('page', 1)

    paginator = Paginator(debtor_r, 10)
    try:
        debtor = paginator.page(page)
    except PageNotAnInteger:
        debtor = paginator.page(1)
    except EmptyPage:
        debtor = paginator.page(paginator.num_pages)

    return render(request, "clientele/debtors.html", {'debtor': debtor})

@login_required
def register(request):
    if request.method == 'POST':
        form = ClienteleForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            name = form.cleaned_data['clientele_name']
            obj.clientele_name = name.upper()
            form.save()
            return redirect('/clientele/clientele')
    else:
        form = ClienteleForm()

    return render(request, "clientele/clientele_form.html", {"form": form, "messages": ''})


@login_required
def clientele_update(request, id):
    if request.method == 'POST':
        pro = Clientele.objects.get(id=id)
        form = ClienteleForm(request.POST, instance=pro)
        if form.is_valid():
            form.save()
            return redirect('/clientele/clientele')
    else:

        pro = Clientele.objects.get(id=id)
        form = ClienteleForm(instance=pro)

    return render(request, "clientele/clientele_update.html", {"form": form, "messages": ''})



class ClienteleDeleteView(LoginRequiredMixin, DeleteView):
    model = Clientele
    success_url = reverse_lazy('clientele:clientele_list')

def getfile(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=clientele.csv'
    clientele = Clientele.objects.all()
    writer = csv.writer(response)
    for c in clientele:
        writer.writerow([c.clientele_name, c.clientele_type, c.clientele_address, c.clientele_email,
                         c.clientele_contact_number, c.clientele_wallet_balance])
    return response
