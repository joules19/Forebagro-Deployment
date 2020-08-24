from .models import ExpenseBasedTransactionForm, ExpenseBasedTransaction, TransactionRecord, CustomerDebtTransaction, \
    CustomerDebtTransactionForm, ForebDebtTransactionForm, SalesTransaction, SalesTransactionForm, ForebDebtTransaction, \
    PurchaseTransaction, PurchaseTransactionForm
from django.core import serializers
from constant.models import Constants
from django.db.models import F


def expectedoil(request):
    obj = Constants.objects.get(constant_name='Expected Oil Const.')
    expected_oil = obj.constant_value
    return {
        'expectedoil': expected_oil
    }

def expectedcake(request):
    obj = Constants.objects.get(constant_name='Expected Cake Const.')
    expected_cake = obj.constant_value
    return {
        'expectedcake': expected_cake
    }

def cakevalue(request):
    obj = Constants.objects.get(constant_name='Cake Value Const.')
    cake_value = obj.constant_value
    return {
        'cakevalue': cake_value
    }

def oilvalue(request):
    obj = Constants.objects.get(constant_name='Oil Value Const.')
    oil_value = obj.constant_value
    return {
        'oilvalue': oil_value
    }


def count_sales(request):
    numberofrecords = SalesTransaction.objects.filter(status__icontains='pending').count()
    return {
        'count_sales': numberofrecords
    }


def count_purchase(request):
    numberofrecords = PurchaseTransaction.objects.filter(status__icontains='pending').count()
    return {
        'count_purchase': numberofrecords
    }


def count_foreb(request):
    numberofrecords = ForebDebtTransaction.objects.filter(status__icontains='pending').count()
    return {
        'count_foreb': numberofrecords
    }


def count_customer(request):
    numberofrecords = CustomerDebtTransaction.objects.filter(status__icontains='pending').count()
    return {
        'count_customer': numberofrecords
    }


def count_expense(request):
    numberofrecords = ExpenseBasedTransaction.objects.filter(status__icontains='pending').count()
    return {
        'count_expense': numberofrecords
    }
