from django.shortcuts import render, redirect
from .models import ExpenseBasedTransactionForm, ExpenseBasedTransaction, TransactionRecord, CustomerDebtTransaction, \
    CustomerDebtTransactionForm, ForebDebtTransactionForm, SalesTransaction, SalesTransactionForm, ForebDebtTransaction, \
    PurchaseTransaction, PurchaseTransactionForm
from clientele.models import Clientele
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.http import HttpResponse, request
from .forms import SummaryForm, PTForm, SLForm, EBForm, CDForm, FDForm, CustomerForm

from constant.models import Constants
from products.models import Product
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import datetime
from django.urls import reverse_lazy
import csv
from django.db.models import Q
from django.core import serializers


# Create your views here.

@login_required
def record(request):
    if request.method == 'POST':
        form = ExpenseBasedTransactionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            clientele_id = form.cleaned_data['clientele_id']
            clientele_name = Clientele.objects.raw('select id,clientele_name from clientele where id=' + clientele_id)[
                0]
            try:
                numy = ExpenseBasedTransaction.objects.latest('id')
                numberofrecords = numy.id
            except:
                numberofrecords = ExpenseBasedTransaction.objects.filter().count()

            obj.clientele_name = clientele_name
            obj.status = 'Pending'
            obj.narration = str(form.cleaned_data['quantity']) + ' of ' + str(clientele_name) + ' @ ' + str(
                form.cleaned_data['rate'])
            generatednumber = int(numberofrecords) + 1
            obj.transaction_reference = 'EB-' + str(generatednumber)
            obj.transaction_type = 'expense-based transaction'
            obj.initiator = request.user.get_username()
            obj.save()

            return render(request, "transactions/eb_transaction_successful.html", )
    else:
        form = ExpenseBasedTransactionForm()

    return render(request, "transactions/eb_transaction_form.html", {"form": form, "messages": ''})


@login_required
def customer(request):
    if request.method == 'POST':
        form = CustomerDebtTransactionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            clientele_id = form.cleaned_data['clientele_name']
            clientele_name = Clientele.objects.raw('select id,clientele_name from clientele where id=' + clientele_id)[
                0]
            obj.clientele_id = clientele_id
            obj.clientele_name = clientele_name
            obj.status = 'Pending'

            try:
                numy = CustomerDebtTransaction.objects.latest('id')
                numberofrecords = numy.id
            except:
                numberofrecords = CustomerDebtTransaction.objects.filter().count()

            generatednumber = int(numberofrecords) + 1
            obj.transaction_reference = 'CD-' + str(generatednumber)
            obj.transaction_type = 'customer-debt transaction'
            obj.initiator = request.user.get_username()
            obj.save()
            return render(request, "transactions/cd_transaction_successful.html", )
    else:
        form = CustomerDebtTransactionForm()

    return render(request, "transactions/cd_transaction_form.html", {"form": form, "messages": ''})


@login_required
def foreb(request):
    if request.method == 'POST':
        form = ForebDebtTransactionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            clientele_id = form.cleaned_data['clientele_name']
            clientele_name = Clientele.objects.raw('select id,clientele_name from clientele where id=' + clientele_id)[
                0]
            obj.clientele_id = clientele_id
            obj.clientele_name = clientele_name

            try:
                numy = ForebDebtTransaction.objects.latest('id')
                numberofrecords = numy.id
            except:
                numberofrecords = ForebDebtTransaction.objects.filter().count()

            generatednumber = int(numberofrecords) + 1
            obj.transaction_reference = 'FD-' + str(generatednumber)
            obj.status = 'pending'
            obj.transaction_type = 'foreb-debt transaction'
            obj.initiator = request.user.get_username()
            obj.save()
            return render(request, "transactions/fd_transaction_successful.html", )
    else:
        form = ForebDebtTransactionForm()

    return render(request, "transactions/fd_transaction_form.html", {"form": form, "messages": ''})


@login_required
def purchase(request):
    if request.method == 'POST':
        form = PurchaseTransactionForm(request.POST, auto_id=True, )
        if form.is_valid():
            obj = form.save(commit=False)
            clientele_id = form.cleaned_data['clientele_name']
            product_id = form.cleaned_data['product_name']
            clientele_name = Clientele.objects.raw('select id,clientele_name from clientele where id=' + clientele_id)[
                0]
            product_name = Product.objects.raw('select id,product_name from products where id=' + product_id)[0]
            obj.clientele_id = clientele_id
            obj.clientele_name = clientele_name
            obj.product_id = product_id
            obj.product_name = product_name
            product_quantity = str(form.cleaned_data['product_quantity'])
            product_rate = str(form.cleaned_data['product_rate'])

            try:
                numy = PurchaseTransaction.objects.latest('id')
                numberofrecords = numy.id
            except:
                numberofrecords = PurchaseTransaction.objects.filter().count()

            generatednumber = int(numberofrecords) + 1
            obj.transaction_reference = 'PC-' + str(generatednumber)
            obj.status = 'pending'
            obj.narration = product_quantity + "kg" + " of " + str(product_name) + " @ " + product_rate
            obj.transaction_type = 'purchase transaction'
            obj.initiator = request.user.get_username()
            obj.save()
            return render(request, "transactions/pc_transaction_successful.html", )
    else:
        form = PurchaseTransactionForm()

    return render(request, "transactions/pc_transaction_form.html", {"form": form, "messages": ''})


@login_required
def sales(request):
    if request.method == 'POST':
        form = SalesTransactionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            clientele_id = form.cleaned_data['clientele_name']
            product_id = form.cleaned_data['product_name']
            clientele_name = Clientele.objects.raw('select id,clientele_name from clientele where id=' + clientele_id)[
                0]
            product_name = Product.objects.raw('select id,product_name from products where id=' + product_id)[0]
            product_quantity = str(form.cleaned_data['product_quantity'])
            product_rate = str(form.cleaned_data['product_rate'])
            obj.clientele_id = clientele_id
            obj.clientele_name = clientele_name
            obj.product_id = product_id
            obj.product_name = product_name

            try:
                numy = SalesTransaction.objects.latest('id')
                numberofrecords = numy.id
            except:
                numberofrecords = SalesTransaction.objects.filter().count()


            generatednumber = int(numberofrecords) + 1
            obj.transaction_reference = 'SA-' + str(generatednumber)

            obj.narration = product_quantity + "tons" + " of " + str(product_name) + " @ " + product_rate
            obj.status = 'pending'
            obj.transaction_type = 'sales transaction'
            obj.initiator = request.user.get_username()
            obj.save()
            return render(request, "transactions/sa_transaction_successful.html", )
    else:
        form = SalesTransactionForm()

    return render(request, "transactions/sa_transaction_form.html", {"form": form, "messages": ''})


@login_required
def showcustomer(request):
    if 'transactions_query' in request.GET:
        transactions = CustomerDebtTransaction.objects.filter(
            clientele_name__icontains=request.GET['transactions_query'])
    else:
        transactions = CustomerDebtTransaction.objects.filter(status__icontains='pending')[:20]

    return render(request, "approve/customer_list.html", {"transactions": transactions, "messages": ''})


@login_required
def showforeb(request):
    if 'transactions_query' in request.GET:
        transactions = ForebDebtTransaction.objects.filter(clientele_name__icontains=request.GET['transactions_query'])
    else:
        transactions = ForebDebtTransaction.objects.filter(status__icontains='pending')[:20]

    return render(request, "approve/foreb_list.html", {"transactions": transactions, "messages": ''})


@login_required
def showsales(request):
    if 'transaction_query' in request.GET:
        transactions = SalesTransaction.objects.filter(clientele_name__icontains=request.GET['transaction_query'])
    else:
        transactions = SalesTransaction.objects.filter(status__icontains='pending')[:20]

    return render(request, "approve/sales_list.html", {"transactions": transactions, "messages": ''})


@login_required
def showpurchase(request):
    if 'transactions_query' in request.GET:
        transactions = PurchaseTransaction.objects.filter(clientele_name__icontains=request.GET['transactions_query'])
    else:
        transactions = PurchaseTransaction.objects.filter(status__icontains='pending')[:20]

    return render(request, "approve/purchase_list.html", {"transactions": transactions, "messages": ''})


@login_required
def showexpense(request):
    if 'transactions_query' in request.GET:
        transactions = ExpenseBasedTransaction.objects.filter(
            clientele_name__icontains=request.GET['transactions_query'])
    else:
        transactions = ExpenseBasedTransaction.objects.filter(status__icontains='pending')[:20]

    return render(request, "approve/expense_list.html", {"transactions": transactions, "messages": ''})


def showcustomer_user(request):
    if 'transactions_query' in request.GET:
        transactions = CustomerDebtTransaction.objects.filter(
            clientele_name__icontains=request.GET['transactions_query'])
    else:
        transactions = CustomerDebtTransaction.objects.filter(status__icontains='pending')
    return render(request, "transactions/customer_list_user.html", {"transactions": transactions, "messages": ''})


@login_required
def showforeb_user(request):
    if 'transactions_query' in request.GET:
        transactions = ForebDebtTransaction.objects.filter(clientele_name__icontains=request.GET['transactions_query'])
    else:
        transactions = ForebDebtTransaction.objects.filter(status__icontains='pending')

    return render(request, "transactions/foreb_list_user.html", {"transactions": transactions, "messages": ''})


@login_required
def showsales_user(request):
    if 'transaction_query' in request.GET:
        transactions = SalesTransaction.objects.filter(clientele_name__icontains=request.GET['transaction_query'])
    else:
        transactions = SalesTransaction.objects.filter(status__icontains='pending')

    return render(request, "transactions/sales_list_user.html", {"transactions": transactions, "messages": ''})


@login_required
def showpurchase_user(request):
    if 'transactions_query' in request.GET:
        transactions = PurchaseTransaction.objects.filter(clientele_name__icontains=request.GET['transactions_query'])
    else:
        transactions = PurchaseTransaction.objects.filter(status__icontains='pending')

    return render(request, "transactions/purchase_list_user.html", {"transactions": transactions, "messages": ''})


@login_required
def showexpense_user(request):
    if 'transactions_query' in request.GET:
        transactions = ExpenseBasedTransaction.objects.filter(
            clientele_name__icontains=request.GET['transactions_query'])
    else:
        transactions = ExpenseBasedTransaction.objects.filter(status__icontains='pending')

    return render(request, "transactions/expense_list_user.html", {"transactions": transactions, "messages": ''})


@login_required
def update_sales(request, id):
    if request.method == 'POST':
        pro = SalesTransaction.objects.get(id=id)
        form = SLForm(request.POST, instance=pro)
        if form.is_valid():
            obj = form.save(commit=False)
            product_name = str(form.cleaned_data['product_name'])
            product_rate = str(form.cleaned_data['product_rate'])
            product_quantity = str(form.cleaned_data['product_quantity'])
            obj.narration = product_quantity + " of " + product_name + " @ " + product_rate
            obj.updated_by = request.user.get_username()
            form.save()

            return redirect('/transactions/sales-transactions')
    else:

        pro = SalesTransaction.objects.get(id=id)
        form = SLForm(instance=pro)

    return render(request, "transactions/update-sales.html", {"form": form, "messages": ''})


@login_required
def update_purchase(request, id):
    if request.method == 'POST':
        pro = PurchaseTransaction.objects.get(id=id)
        form = PTForm(request.POST, instance=pro)
        if form.is_valid():
            obj = form.save(commit=False)
            product_name = str(form.cleaned_data['product_name'])
            product_rate = str(form.cleaned_data['product_rate'])
            product_quantity = str(form.cleaned_data['product_quantity'])
            obj.narration = product_quantity + " of " + product_name + " @ " + product_rate
            obj.updated_by = request.user.get_username()
            form.save()
            return redirect('/transactions/purchase-transactions')
    else:

        pro = PurchaseTransaction.objects.get(id=id)
        form = PTForm(instance=pro)

    return render(request, "transactions/update-purchase.html", {"form": form, "messages": ''})


@login_required
def update_expense(request, id):
    if request.method == 'POST':
        pro = ExpenseBasedTransaction.objects.get(id=id)
        form = EBForm(request.POST, instance=pro)
        if form.is_valid():
            obj = form.save(commit=False)
            clientele_name = str(form.cleaned_data['clientele_name'])
            obj.clientele_name = clientele_name
            obj.narration = str(form.cleaned_data['quantity']) + ' of ' + str(clientele_name) + ' @ ' + str(
                form.cleaned_data['rate'])
            obj.updated_by = request.user.get_username()
            form.save()
            return redirect('/transactions/expense-transactions')
    else:

        pro = ExpenseBasedTransaction.objects.get(id=id)
        form = EBForm(instance=pro)

    return render(request, "transactions/update-expense.html", {"form": form, "messages": ''})


@login_required
def update_foreb(request, id):
    if request.method == 'POST':
        pro = ForebDebtTransaction.objects.get(id=id)
        form = FDForm(request.POST, instance=pro)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.updated_by = request.user.get_username()
            form.save()
            return redirect('/transactions/foreb-transactions')
    else:

        pro = ForebDebtTransaction.objects.get(id=id)
        form = FDForm(instance=pro)

    return render(request, "transactions/update-foreb.html", {"form": form, "messages": ''})


@login_required
def update_customer(request, id):
    if request.method == 'POST':
        pro = CustomerDebtTransaction.objects.get(id=id)
        form = CDForm(request.POST, instance=pro)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.updated_by = request.user.get_username()
            form.save()
            return redirect('/transactions/customer-transactions')
    else:

        pro = CustomerDebtTransaction.objects.get(id=id)
        form = CDForm(instance=pro)

    return render(request, "transactions/update-customer.html", {"form": form, "messages": ''})


class SalesDeleteView(LoginRequiredMixin, DeleteView):
    model = SalesTransaction
    success_url = reverse_lazy('transactions:show_sales_user')


class PurchaseDeleteView(LoginRequiredMixin, DeleteView):
    model = PurchaseTransaction
    success_url = reverse_lazy('transactions:show_purchase_user')


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = ExpenseBasedTransaction
    success_url = reverse_lazy('transactions:show_expense_user')


class ForebDeleteView(LoginRequiredMixin, DeleteView):
    model = ForebDebtTransaction
    success_url = reverse_lazy('transactions:show_foreb_user')


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomerDebtTransaction
    success_url = reverse_lazy('transactions:show_customer_user')


@login_required
def customer_details(request, id):
    transactions = CustomerDebtTransaction.objects.get(id=id)
    context = {
        "transactions": transactions,
        "messages": '',
        "id": id,
    }
    return render(request, "transactions/approve_customer.html", context)


@login_required
def foreb_details(request, id):
    transactions = ForebDebtTransaction.objects.get(id=id)
    context = {
        "transactions": transactions,
        "messages": '',
        "id": id,
    }
    return render(request, "transactions/approve_foreb.html", context)


@login_required
def sales_details(request, id):
    transactions = SalesTransaction.objects.get(id=id)
    context = {
        "transactions": transactions,
        "messages": '',
        "id": id,
    }
    return render(request, "transactions/approve_sales.html", context)


@login_required
def purchase_details(request, id):
    transactions = PurchaseTransaction.objects.get(id=id)
    context = {
        "transactions": transactions,
        "messages": '',
        "id": id,
    }
    return render(request, "transactions/approve_purchase.html", context)


@login_required
def expense_details(request, id):
    transactions = ExpenseBasedTransaction.objects.get(id=id)
    context = {
        "transactions": transactions,
        "messages": '',
        "id": id,
    }
    return render(request, "transactions/approve_expense.html", context)


@login_required
def customer_approve(request, id):
    pro = CustomerDebtTransaction.objects.get(id=id)
    pro.status = 'approved'
    pro.original_approved_date = datetime.datetime.now()
    pro.date_approved = datetime.datetime.now()
    types = pro.transaction_type
    ref = pro.transaction_reference
    clientele_id = pro.clientele_id
    transaction_cost = pro.amount_paid
    pro.save()
    transaction = TransactionRecord()
    transaction.clientele_id = clientele_id
    transaction.transaction_reference = ref
    transaction.transaction_amount = transaction_cost
    transaction.transaction_approved_date = datetime.datetime.now()
    transaction.transaction_type = types
    transaction.transaction_status = 'approved'
    transaction.approved_by = request.user.get_username()
    transaction.save()
    return redirect('/transactions/customer_transactions')


@login_required
def foreb_approve(request, id):
    pro = ForebDebtTransaction.objects.get(id=id)
    pro.status = 'approved'
    pro.original_approved_date = datetime.datetime.now()
    pro.date_approved = datetime.datetime.now()
    types = pro.transaction_type
    ref = pro.transaction_reference
    clientele_id = pro.clientele_id
    transaction_cost = pro.amount_paid
    pro.save()
    transaction = TransactionRecord()
    transaction.transaction_amount = transaction_cost
    transaction.clientele_id = clientele_id
    transaction.transaction_reference = ref
    transaction.transaction_approved_date = datetime.datetime.now()
    transaction.transaction_type = types
    transaction.transaction_status = 'approved'
    transaction.approved_by = request.user.get_username()
    transaction.save()
    return redirect('/transactions/foreb_transactions')


@login_required
def sales_approve(request, id):
    pro = SalesTransaction.objects.get(id=id)
    pro.status = 'approved'
    pro.original_approved_date = datetime.datetime.now()
    pro.date_approved = datetime.datetime.now()
    types = pro.transaction_type
    ref = pro.transaction_reference
    clientele_id = pro.clientele_id
    transaction_cost = pro.transaction_income
    pro.save()
    transaction = TransactionRecord()
    transaction.transaction_reference = ref
    transaction.clientele_id = clientele_id
    transaction.transaction_amount = transaction_cost
    transaction.transaction_approved_date = datetime.datetime.now()
    transaction.transaction_type = types
    transaction.transaction_status = 'approved'
    transaction.approved_by = request.user.get_username()
    transaction.save()
    return redirect('/transactions/sales_transactions')


@login_required
def purchase_approve(request, id):
    pro = PurchaseTransaction.objects.get(id=id)
    pro.status = 'approved'
    pro.original_approved_date = datetime.datetime.now()
    pro.date_approved = datetime.datetime.now()
    types = pro.transaction_type
    ref = pro.transaction_reference
    clientele_id = pro.clientele_id
    transaction_cost = pro.transaction_cost
    pro.save()
    transaction = TransactionRecord()
    transaction.clientele_id = clientele_id
    transaction.transaction_reference = ref
    transaction.transaction_amount = transaction_cost
    transaction.transaction_approved_date = datetime.datetime.now()
    transaction.transaction_type = types
    transaction.transaction_status = 'approved'
    transaction.approved_by = request.user.get_username()
    transaction.save()
    return redirect('/transactions/purchase_transactions')


@login_required
def expense_approve(request, id):
    pro = ExpenseBasedTransaction.objects.get(id=id)
    pro.status = 'approved'
    pro.original_approved_date = datetime.datetime.now()
    pro.date_approved = datetime.datetime.now()
    types = pro.transaction_type
    ref = pro.transaction_reference
    clientele_id = pro.clientele_id
    transaction_cost = pro.total_cost
    pro.save()
    transaction = TransactionRecord()
    transaction.clientele_id = clientele_id
    transaction.transaction_reference = ref
    transaction.transaction_amount = transaction_cost
    transaction.transaction_approved_date = datetime.datetime.now()
    transaction.transaction_type = types
    transaction.transaction_status = 'approved'
    transaction.approved_by = request.user.get_username()
    transaction.save()
    return redirect('/transactions/expense_transactions')


def is_valid_queryparam(param):
    return param != '' and param is not None


start_date = []
end_date = []


@login_required
def view_summary(request):
    if request.method == 'POST':
        form = SummaryForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            s = start_date.append(start)
            start_date.append(end)
    else:
        form = SummaryForm()

    return render(request, "transactions/view_summary.html", {"form": form, "messages": ''})


@login_required
def summary(request):
    if request.method == 'POST':
        form = SummaryForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']

            qz = Constants.objects.get(constant_name='Batch-Tracker-Default-Value')

            qy = Constants.objects.get(constant_name='Batch-Tracker-Rollover-Value')

            qp = TransactionRecord.objects.raw(
                "SELECT 1 as id, SUM(expected_oil) AS expected_oil , SUM(transaction_cost) AS transaction_cost, Sum(transaction_income) AS transaction_income, Sum(expected_cake) AS expected_cake from " +
                "(SELECT 1 as id, SUM(expected_oil) AS expected_oil , SUM(transaction_cost) AS transaction_cost, Sum(transaction_income) AS transaction_income, Sum(expected_cake) AS expected_cake from ((select 1 as id, A.id AS TXID, B.id AS P_ID,B.expected_oil AS expected_oil, " +
                "B.expected_cake AS expected_cake, B.transaction_cost AS transaction_cost, B.transaction_income AS transaction_income from transactions_record AS A " +
                "left join purchase_transactions AS B on A.transaction_reference = B.transaction_reference where B.date_initiated < %s and B.status = 'approved' " +
                "UNION " +
                "select 1 as id, A.id AS TXID, C.id AS S_ID, C.expected_oil AS expected_oil,C.expected_cake AS expected_cake, C.transaction_cost AS transaction_cost, C.transaction_income AS transaction_income from transactions_record AS A" +
                " left join sales_transactions AS C on A.transaction_reference = C.transaction_reference where C.date_initiated <%s and C.status = 'approved' " +
                "UNION " +
                "select 1 as id, A.id AS TXID, D.id AS S_ID, 0 AS expected_oil,0 AS expected_cake, D.total_cost AS transaction_cost, 0 AS transaction_income from transactions_record AS A left join expense_based_transactions AS D " +
                "on A.transaction_reference = D.transaction_reference where D.date_initiated <%s and D.status = 'approved')))",
                [start, start, start])

            qr = TransactionRecord.objects.raw(
                "SELECT 1 as id, SUM(expected_oil) AS expected_oil , SUM(transaction_cost) AS transaction_cost, Sum(transaction_income) AS transaction_income, Sum(expected_cake) AS expected_cake from " +
                "(SELECT 1 as id, SUM(expected_oil) AS expected_oil , SUM(transaction_cost) AS transaction_cost, Sum(transaction_income) AS transaction_income, Sum(expected_cake) AS expected_cake from ((select 1 as id, A.id AS TXID, B.id AS P_ID,B.expected_oil AS expected_oil, " +
                "B.expected_cake AS expected_cake, B.transaction_cost AS transaction_cost, B.transaction_income AS transaction_income from transactions_record AS A " +
                "left join purchase_transactions AS B on A.transaction_reference = B.transaction_reference where B.date_initiated <= %s and B.status = 'approved' " +
                "UNION " +
                "select 1 as id, A.id AS TXID, C.id AS S_ID, C.expected_oil AS expected_oil,C.expected_cake AS expected_cake, C.transaction_cost AS transaction_cost, C.transaction_income AS transaction_income from transactions_record AS A" +
                " left join sales_transactions AS C on A.transaction_reference = C.transaction_reference where C.date_initiated <=%s and C.status = 'approved' " +
                "UNION " +
                "select 1 as id, A.id AS TXID, D.id AS S_ID, 0 AS expected_oil,0 AS expected_cake, D.total_cost AS transaction_cost, 0 AS transaction_income from transactions_record AS A left join expense_based_transactions AS D " +
                "on A.transaction_reference = D.transaction_reference where D.date_initiated <=%s and D.status = 'approved')))",
                [end, end, end])

            qs = TransactionRecord.objects.raw(
                "SELECT 1 as id, transaction_reference,date_initiated,clientele_name,product_rate, product_name,product_quantity,quantity_value,expected_oil, " +
                "t_expected_oil,t_cost,0 AS t_income, 0 AS BT,0 AS BB,0 AS BC,0 AS CPT,expected_cake, transaction_income,transaction_cost FROM (Select 1 as id, A.id AS TXID, B.id AS P_ID, B.transaction_reference AS " +
                "transaction_reference,B.date_initiated AS date_initiated,B.clientele_name AS clientele_name,B.product_rate AS product_rate,B.product_name AS product_name,B.product_quantity As product_quantity, B.quantity_value AS quantity_value," +
                "B.expected_oil AS expected_oil, 0 as t_expected_oil, 0 as t_cost,0 AS t_income, 0 AS BT,0 AS BB,0 AS BC,0 AS CPT, B.expected_cake AS expected_cake, B.transaction_income AS transaction_income,B.transaction_cost AS transaction_cost " +
                "from transactions_record AS A left join purchase_transactions B ON A.transaction_reference= B.transaction_reference Where B.status='approved' and B.date_initiated >=%s and B.date_initiated <= %s" +
                "UNION " +
                "Select 1 as id, A.id AS TXID, C.id AS S_ID,A.transaction_reference AS transaction_reference,C.date_initiated AS date_initiated,C.clientele_name AS clientele_name,C.product_rate AS product_rate,C.product_name AS product_name,C.product_quantity As product_quantity, C.quantity_value AS quantity_value, " +
                "C.expected_oil AS expected_oil, 0 as t_expected_oil, 0 as t_cost,0 AS t_income, 0 AS BT,0 AS BB,0 AS BC,0 AS CPT, C.expected_cake AS expected_cake, C.transaction_income AS transaction_income,C.transaction_cost AS transaction_cost " +
                "from transactions_record AS A left join sales_transactions C ON A.transaction_reference= C.transaction_reference Where C.status='approved' and C.date_initiated >=%s and C.date_initiated <= %s " +
                "UNION " +
                "Select 1 as id, Z.id AS TXID, D.id AS E_ID, D.transaction_reference AS transaction_reference,D.date_initiated AS date_initiated,D.clientele_name AS clientele_name,D.rate AS product_rate, 0 AS product_name,D.quantity AS product_quantity, 0 AS quantity_value," +
                "0 AS expected_oil,0 as t_expected,0 AS t_cost,0 AS t_income, 0 AS BT,0 AS BB,0 AS BC,0 AS CPT, 0 AS expected_cake, 0 AS transaction_income, D.total_cost AS transaction_cost from transactions_record Z" +
                " left join expense_based_transactions D ON Z.transaction_reference= D.transaction_reference Where D.status='approved' and D.date_initiated >=%s and D.date_initiated <= %s" +
                ") ORDER by date_initiated", [start, end, start, end, start, end])

            qss = list(qs)

            L = []
            X = []
            BTs = []
            BatchHolder = []

            BBs = []
            BCs = []
            CPTs = []
            M = []
            Y = []

            N = []
            Z = []

            for q in qs:
                L.append(q.expected_oil)
                M.append(q.transaction_cost)
                N.append(q.transaction_income)

            for q in qp:
                openingbalSum = (q.expected_oil)

                if openingbalSum is None:
                    openingbalSum = 0
                for l in L:
                    openingbalSum = openingbalSum + l
                    X.append(openingbalSum)
            i = 0
            for q in qss:
                q.t_expected_oil = X[i]
                i = i + 1

            for q in qp:
                openingbalSum = (q.transaction_cost)

                if openingbalSum is None:
                    openingbalSum = 0
                    BatchHolder.append(0)
                else:
                    BatchHolder.append(q.transaction_cost)

                for m in M:
                    openingbalSum = openingbalSum + m

                    Y.append(openingbalSum)
            i = 0
            for q in qss:
                q.t_cost = Y[i]
                i = i + 1

            for q in qp:
                openingbalSum = (q.transaction_income)
                if openingbalSum is None:
                    openingbalSum = 0
                for n in N:
                    openingbalSum = openingbalSum + n
                    Z.append(openingbalSum)
            i = 0
            for q in qss:
                q.t_income = Z[i]
                i = i + 1

            InitBts = float(qz.constant_value)

            for l in L:
                newVal = InitBts + l
                if (l > 0):

                    if (newVal > float(qy.constant_value)):
                        if not BBs:
                            BBs.append(0)
                            InitBts = l
                            BTs.append(l)


                        else:
                            BTs.append(l)
                            BBs[-1] = 1
                            BBs.append(0)
                            InitBts = l
                    else:
                        BBs.append(0)
                        BTs.append(newVal)
                        InitBts = newVal
                else:
                    BTs.append(InitBts)
                    BBs.append(0)

            i = 0
            for q in qss:
                q.BT = BTs[i]
                q.BB = BBs[i]
                if q.BB == 1:

                    q.BC = Y[i] - BatchHolder[-1]
                    BatchHolder.append(Y[i])

                    q.CPT = q.BC / q.BT
                else:
                    q.BC = 0
                    q.CPT = 0

                i = i + 1

            qyy = float(qy.constant_value)
            context = {
                "qs": qss,
                "qp": qp,
                "qy": qyy,
                "qr": qr,
                "start": start,
                "end": end,

                "messages": '',
            }

            return render(request, "transactions/summary.html", context)


@login_required
def view_customer_statement(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            s = start_date.append(start)
            start_date.append(end)
    else:
        form = CustomerForm()

    return render(request, "transactions/view_customer_statement.html", {"form": form, "messages": ''})


@login_required
def customer_statement(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            clientele_name = Clientele.objects.raw('select id,clientele_name from clientele where id=' + name)[
                0]
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            names = clientele_name


            qa = Clientele.objects.get(id=name)


            qb = TransactionRecord.objects.raw(
                "Select 1 as id, SUM(OUTSTANDING) AS outstanding FROM (Select 0 AS TRANSACTION_COST, sales.transaction_income AS INCOME, sales.amount_paid AS AMOUNT_PAID, (sales.amount_paid-sales.transaction_income) AS OUTSTANDING, CASE WHEN (sales.transaction_income-sales.amount_paid) >= 0 " +
                "THEN 'DEBIT' ELSE 'CREDIT' END AS LEG_TYPE from transactions_record Tr Left join clientele client On Tr.clientele_id= client.id Left Join sales_transactions sales ON Tr.transaction_reference= sales.transaction_reference Where Tr.clientele_id = %s " +
                "and sales.date_initiated < %s and Tr.transaction_status='approved' " +
                "UNION " +
                "Select  PT.transaction_cost AS COST, 0 AS TRANSACTION_INCOME,PT.amount_paid AS AMOUNT_PAID,(PT.transaction_cost-PT.amount_paid) AS OUTSTANDING, CASE WHEN (PT.transaction_cost-PT.amount_paid) >= 0 THEN 'CREDIT' ELSE 'DEBIT'  END AS LEG_TYPE " +
                "from transactions_record Tr Left join clientele client On Tr.clientele_id= client.id Left Join purchase_transactions PT ON Tr.transaction_reference= PT.transaction_reference Where Tr.clientele_id = %s and PT.date_initiated < %s and Tr.transaction_status='approved' " +
                "UNION " +
                "Select  CDT.amount_paid AS COST, 0 AS TRANSACTION_INCOME,CDT.amount_paid AS AMOUNT_PAID,(CDT.amount_paid) AS OUTSTANDING, 'CREDIT' AS LEG_TYPE from transactions_record Tr Left join clientele client On Tr.clientele_id= client.id " +
                "Left Join customer_debt_transactions CDT ON Tr.transaction_reference= CDT.transaction_reference Where Tr.clientele_id = %s and CDT.date_initiated < %s  and Tr.transaction_status='approved' " +
                "UNION " +
                "Select  0 AS COST, FDT.amount_paid AS TRANSACTION_INCOME,FDT.amount_paid AS AMOUNT_PAID,(FDT.amount_paid * -1) AS OUTSTANDING, 'DEBIT' AS LEG_TYPE from transactions_record Tr	Left join clientele client " +
                "On Tr.clientele_id= client.id Left Join foreb_debt_transactions FDT ON Tr.transaction_reference= FDT.transaction_reference Where Tr.clientele_id = %s and FDT.date_initiated < %s  and Tr.transaction_status='approved')",
                [name,start,name, start, name,start,name, start])
            qbb = list(qb)
            B = []
            for q in qbb:
                if q.outstanding is None:
                    B.append(0)
                else:
                    B.append(q.outstanding)


            qc = TransactionRecord.objects.raw(
                "Select 1 as id, SUM(OUTSTANDING) as outstanding FROM (Select 0 AS TRANSACTION_COST, sales.transaction_income AS INCOME, sales.amount_paid AS AMOUNT_PAID, (sales.amount_paid-sales.transaction_income) AS OUTSTANDING, CASE WHEN (sales.transaction_income-sales.amount_paid) >= 0 " +
                "THEN 'DEBIT' ELSE 'CREDIT'  END AS LEG_TYPE from transactions_record Tr Left join clientele client On Tr.clientele_id= client.id Left Join sales_transactions sales ON Tr.transaction_reference= sales.transaction_reference Where Tr.clientele_id = %s " +
                "and sales.date_initiated <=%s  and Tr.transaction_status='approved'" +
                " UNION "+
                "Select  PT.transaction_cost AS COST, 0 AS TRANSACTION_INCOME,PT.amount_paid AS AMOUNT_PAID,(PT.transaction_cost-PT.amount_paid) AS OUTSTANDING, CASE WHEN (PT.transaction_cost-PT.amount_paid) >= 0 THEN 'CREDIT' ELSE 'DEBIT'  END AS LEG_TYPE" +
                " from transactions_record Tr Left join clientele client On Tr.clientele_id= client.id Left Join purchase_transactions PT ON Tr.transaction_reference= PT.transaction_reference Where Tr.clientele_id = %s and PT.date_initiated <= %s  and Tr.transaction_status='approved' " +
                "UNION " +
                "Select  CDT.amount_paid AS COST, 0 AS TRANSACTION_INCOME,CDT.amount_paid AS AMOUNT_PAID,(CDT.amount_paid) AS OUTSTANDING, 'CREDIT' AS LEG_TYPE from transactions_record Tr Left join clientele client On Tr.clientele_id= client.id " +
                " Left Join customer_debt_transactions CDT ON Tr.transaction_reference= CDT.transaction_reference Where Tr.clientele_id = %s and CDT.date_initiated <= %s  and Tr.transaction_status='approved'" +
                " UNION " +
                "Select  0 AS COST, FDT.amount_paid AS TRANSACTION_INCOME,FDT.amount_paid AS AMOUNT_PAID,(FDT.amount_paid * -1) AS OUTSTANDING, 'DEBIT' AS LEG_TYPE from transactions_record Tr	Left join clientele client " +
                "On Tr.clientele_id= client.id Left Join foreb_debt_transactions FDT ON Tr.transaction_reference= FDT.transaction_reference Where Tr.clientele_id = %s and FDT.date_initiated <= %s  and Tr.transaction_status='approved')",
                [name, end, name, end, name, end,  name, end])
            qcc = list(qc)
            C = []
            for q in qcc:
                if q.outstanding is None:
                    C.append(0)
                else:
                    C.append(q.outstanding)

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
                [name,name,name,name])
            qjj = list(qj)
            J = []
            for q in qjj:
                if q.outstanding is None:
                    J.append(0)
                else:
                    J.append(q.outstanding)

            qd = TransactionRecord.objects.raw(
                "Select 1 as id,DATE_INITIATED,T_TYPE,narration,COST,TRANSACTION_INCOME,AMOUNT_PAID,OUTSTANDING,LEG_TYPE,CR,DR,balance from (Select sales.date_initiated AS DATE_INITIATED,sales.transaction_type AS T_TYPE,sales.narration as narration, sales.transaction_income AS COST, sales.transaction_income AS TRANSACTION_INCOME, sales.amount_paid AS AMOUNT_PAID, (sales.amount_paid - sales.transaction_income) AS OUTSTANDING, CASE WHEN (sales.transaction_income-sales.amount_paid) >= 0 " +
                "THEN 'DEBIT' ELSE 'CREDIT' END AS LEG_TYPE,'' AS CR, '' AS DR, 0 AS balance from transactions_record Tr Left join clientele client On Tr.clientele_id= client.id Left Join sales_transactions sales ON Tr.transaction_reference= sales.transaction_reference Where Tr.clientele_id = %s " +
                "and sales.date_initiated >= %s and sales.date_initiated <= %s and Tr.transaction_status='approved' " +
                "UNION " +
                "Select PT.date_initiated AS DATE_INITIATED,PT.transaction_type AS T_TYPE,PT.narration as narration,PT.transaction_cost AS COST, 0 AS TRANSACTION_INCOME,PT.amount_paid AS AMOUNT_PAID,(PT.transaction_cost-PT.amount_paid) AS OUTSTANDING, CASE WHEN (PT.transaction_cost-PT.amount_paid) >= 0 THEN 'CREDIT' ELSE 'DEBIT'  END AS LEG_TYPE,'' AS CR, '' AS DR, 0 AS balance " +
                "from transactions_record Tr Left join clientele client On Tr.clientele_id= client.id Left Join purchase_transactions PT ON Tr.transaction_reference= PT.transaction_reference Where Tr.clientele_id = %s and PT.date_initiated >= %s and PT.date_initiated <= %s and Tr.transaction_status='approved' " +
                "UNION " +
                "Select  CDT.date_initiated AS DATE_INITIATED,CDT.transaction_type AS T_TYPE,CDT.narration as narration,CDT.amount_paid AS COST, 0 AS TRANSACTION_INCOME,CDT.amount_paid AS AMOUNT_PAID,(CDT.amount_paid) AS OUTSTANDING, 'CREDIT' AS LEG_TYPE,'' AS CR, '' AS DR, 0 AS balance from transactions_record Tr Left join clientele client On Tr.clientele_id= client.id " +
                "Left Join customer_debt_transactions CDT ON Tr.transaction_reference= CDT.transaction_reference Where Tr.clientele_id = %s and CDT.date_initiated >= %s and CDT.date_initiated <= %s and Tr.transaction_status='approved' " +
                "UNION "+
                "Select FDT.date_initiated AS DATE_INITIATED,FDT.transaction_type AS T_TYPE,FDT.narration as narration, FDT.amount_paid AS COST, FDT.amount_paid AS TRANSACTION_INCOME,FDT.amount_paid AS AMOUNT_PAID,(FDT.amount_paid * -1) AS OUTSTANDING, 'DEBIT' AS LEG_TYPE,'' AS CR, '' AS DR, 0 AS balance from transactions_record Tr	Left join clientele client " +
                "On Tr.clientele_id= client.id Left Join foreb_debt_transactions FDT ON Tr.transaction_reference= FDT.transaction_reference Where Tr.clientele_id = %s and FDT.date_initiated >= %s  and FDT.date_initiated <= %s and Tr.transaction_status='approved') order by date_initiated",
                [name,start, end,name, start, end,name, start, end,name, start, end])

            qdd = list(qd)

            fullopeningbalanceATSTART = qa.default_wallet_balance + B[0]


            fullclosingbalanceATEND = qa.default_wallet_balance + C[0]


            currentbalance = qa.default_wallet_balance + J[0]

            newBalance = fullopeningbalanceATSTART

            for q in qdd:
                newBalance = newBalance + float(q.OUTSTANDING)
                q.balance = newBalance
                if q.LEG_TYPE == 'CREDIT':
                    q.CR = str(q.OUTSTANDING)
                else:
                    q.DR = str(q.OUTSTANDING)


            context = {

                "end": end,
                "start": start,
                "messages": '',
                'names':names,
                "qdd": qdd,
                "OpeningBalanceAtStart": fullopeningbalanceATSTART,
                "OpeningBalanceAtEnd": fullclosingbalanceATEND,
                "CustomerAddress": qa.clientele_address,
                "CustomerPhone": qa.clientele_contact_number,
                "CurrentBalance": currentbalance
            }

            return render(request, "transactions/customer_statement.html", context)


class HomePage(TemplateView):
    template_name = "transactions/transactions_tray.html"