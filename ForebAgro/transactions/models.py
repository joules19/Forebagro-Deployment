from django.db import models
from django.db.models import Q
from django.core.validators import validate_comma_separated_integer_list
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, TextInput, CharField, NumberInput, Select, ChoiceField
from django import forms
from clientele.models import Clientele
from products.models import Product
from django.contrib.admin.widgets import AdminDateWidget


# Create your models here.

class ExpenseBasedTransaction(models.Model):
    date_initiated = models.DateField(max_length=30, null=True)
    clientele_name = models.CharField(max_length=20)
    rate = models.IntegerField(null=True, )
    quantity = models.IntegerField(null=True)
    narration = models.CharField(max_length=100)
    total_cost = models.IntegerField(null=True)
    transaction_reference = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    original_approved_date = models.DateTimeField(max_length=30, null=True)
    date_approved = models.DateTimeField(max_length=30, null=True)
    transaction_type = models.CharField(max_length=100, null=True)
    clientele_id = models.IntegerField(null=True)
    initiator = models.CharField(max_length=20, null=True, default="admin")
    updated_by = models.CharField(max_length=20, null=True, default="admin")

    class Meta:
        db_table = "expense_based_transactions"

    def __str__(self):
        return self.transaction_reference + " - " + self.clientele_name


eb_main = []


class ExpenseBasedTransactionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExpenseBasedTransactionForm, self).__init__(*args, **kwargs)
        clientele_id = Clientele.objects.filter(clientele_type__icontains='eb-client').values_list("id",
                                                                                                   "clientele_name")
        eb_main = []
        for i in clientele_id:
            k = list(i)
            k[0] = str(k[0])
            l = (tuple(k))
            eb_main.append(l)
        eb_mains = [('', 'SELECT')] + eb_main
        self.fields['clientele_id'] = ChoiceField(choices=eb_mains, label='Expensed-Based Client')

    class Meta:
        model = ExpenseBasedTransaction
        # fields = '__all__' #to include all the fields in the form

        # specify what fields to be included in the form
        fields = ['date_initiated', 'clientele_id', 'rate',
                  'quantity', 'total_cost']

        widgets = {
            'date_initiated': AdminDateWidget(),
            'rate': NumberInput(attrs={'class': 'form-control', }),
            'quantity': NumberInput(attrs={'class': 'form-control', }),
            'total_cost': NumberInput(attrs={'class': 'form-control', 'readOnly': True}),
        }

        labels = {
            'date_initiated': _('Date Initiated'),
            'clientele_id': _('Expensed-Based Client'),
            'rate': _('Rate'),
            'quantity': _('Quantity'),
            'total_cost': _('Total Cost'),
        }


class CustomerDebtTransaction(models.Model):
    narration_choice = [('part payment', 'Part Payment of Money Owed'), ('full payment', 'Full Payment of Money Owed')]
    date_initiated = models.DateField(max_length=30, null=True)
    transaction_type = models.CharField(max_length=100, null=True)
    transaction_reference = models.CharField(max_length=20)
    clientele_id = models.IntegerField(null=True)
    clientele_name = models.CharField(max_length=20)
    amount_paid = models.IntegerField(null=True)
    status = models.CharField(max_length=20, null=True)
    narration = models.CharField(max_length=100, choices=narration_choice)
    comments = models.CharField(max_length=100)
    original_approved_date = models.DateTimeField(max_length=30, null=True)
    date_approved = models.DateTimeField(max_length=30, null=True)
    initiator = models.CharField(max_length=20, null=True, default="admin")
    updated_by = models.CharField(max_length=20, null=True, default="admin")

    class Meta:
        db_table = "customer_debt_transactions"

    def __str__(self):
        return self.transaction_reference + " - " + self.clientele_name


cd_main = []


class CustomerDebtTransactionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerDebtTransactionForm, self).__init__(*args, **kwargs)
        clientele_id = Clientele.objects.exclude(clientele_type__icontains='eb-client').values_list("id",
                                                                                                    "clientele_name")

        cd_main = []
        for i in clientele_id:
            k = list(i)
            k[0] = str(k[0])
            l = (tuple(k))
            cd_main.append(l)
        cd_mains = [('', 'SELECT')] + cd_main
        self.fields['clientele_name'] = ChoiceField(choices=cd_mains, label='Clientele Name')

    class Meta:
        model = CustomerDebtTransaction
        # fields = '__all__' #to include all the fields in the form

        # specify what fields to be included in the form
        fields = ['date_initiated', 'clientele_name', 'narration', 'comments', 'amount_paid']

        widgets = {
            'amount_paid': NumberInput(attrs={'class': 'form-control'}),
            'narration': Select(attrs={'class': 'form-control'}),
            'comments': TextInput(attrs={'class': 'form-control'}),
            'date_initiated': AdminDateWidget(),
        }

        labels = {
            'date_initiated': _('Date Initiated'),
            'narration': _('Narration'),
            'comments': _('Comments'),
            'amount_paid': _('Amount Paid'),
        }


class ForebDebtTransaction(models.Model):
    narration_choice = [('part payment', 'Part Payment of Money Owed Customer'),
                        ('full payment', 'Full Payment of Money Owed Customer')]

    date_initiated = models.DateField(max_length=30, null=True)
    transaction_type = models.CharField(max_length=100, null=True)
    transaction_reference = models.CharField(max_length=20)
    clientele_id = models.IntegerField(null=True)
    clientele_name = models.CharField(max_length=20)
    amount_paid = models.IntegerField(null=True)
    status = models.CharField(max_length=20, null=True)
    narration = models.CharField(max_length=100, choices=narration_choice)
    comments = models.CharField(max_length=100)
    original_approved_date = models.DateTimeField(max_length=30, null=True)
    date_approved = models.DateTimeField(max_length=30, null=True)
    initiator = models.CharField(max_length=20, null=True, default="admin")
    updated_by = models.CharField(max_length=20, null=True, default="admin")

    class Meta:
        db_table = "foreb_debt_transactions"

    def __str__(self):
        return self.transaction_reference + " - " + self.clientele_name


fd_main = []


class ForebDebtTransactionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ForebDebtTransactionForm, self).__init__(*args, **kwargs)
        clientele_id = Clientele.objects.exclude(clientele_type__icontains='eb-client').values_list("id",
                                                                                                    "clientele_name")

        fd_main = []
        for i in clientele_id:
            k = list(i)
            k[0] = str(k[0])
            l = (tuple(k))
            fd_main.append(l)
        fd_mains = [('', 'SELECT')] + fd_main
        self.fields['clientele_name'] = ChoiceField(choices=fd_mains, label='Clientele Name')

    class Meta:
        model = ForebDebtTransaction
        # fields = '__all__' #to include all the fields in the form

        # specify what fields to be included in the form
        fields = ['date_initiated', 'clientele_name', 'narration', 'comments', 'amount_paid']

        widgets = {
            'amount_paid': NumberInput(attrs={'class': 'form-control'}),
            'narration': Select(attrs={'class': 'form-control'}),
            'comments': TextInput(attrs={'class': 'form-control'}),
            'date_initiated': AdminDateWidget(),
        }

        labels = {
            'date_initiated': _('Date Initiated'),
            'narration': _('Narration'),
            'comments': _('Comments'),
            'amount_paid': _('Amount Paid'),
        }


class PurchaseTransaction(models.Model):
    date_initiated = models.DateField(max_length=30, null=True)
    transaction_type = models.CharField(max_length=100, null=True)
    transaction_reference = models.CharField(max_length=20, null=True)
    clientele_id = models.IntegerField(null=True, )
    clientele_name = models.CharField(max_length=100)
    product_id = models.IntegerField(null=True)
    product_name = models.CharField(max_length=100)
    narration = models.CharField(max_length=100)
    product_quantity = models.IntegerField(null=True)
    product_discount = models.IntegerField(null=True, blank=True)
    product_rate = models.IntegerField(null=True)
    deductions = models.IntegerField(null=True, blank=True)
    quantity_value = models.IntegerField(null=True)
    expected_oil = models.FloatField(null=True, blank=True)
    expected_cake = models.FloatField(null=True, blank=True)
    cake_value = models.FloatField(null=True, blank=True)
    diesel_rate = models.IntegerField(null=True, blank=True)
    diesel_litres = models.IntegerField(null=True, blank=True)
    diesel_value = models.IntegerField(null=True, blank=True)
    gen_diesel_litres = models.IntegerField(null=True, blank=True)
    gen_diesel_rate = models.IntegerField(null=True, blank=True)
    gen_diesel_value = models.IntegerField(null=True, blank=True)
    other_costs = models.FloatField(null=True, blank=True)
    transaction_income = models.IntegerField(null=True)
    transaction_cost = models.IntegerField(null=True)
    waybill_number = models.IntegerField(null=True, blank=True)
    amount_paid = models.IntegerField(null=True, )
    original_approved_date = models.DateTimeField(max_length=30, null=True)
    date_approved = models.DateTimeField(max_length=30, null=True)
    status = models.CharField(max_length=20, null=True)
    initiator = models.CharField(max_length=20, null=True, default="admin")
    updated_by = models.CharField(max_length=20, null=True, default="admin")

    class Meta:
        db_table = "purchase_transactions"

    def __str__(self):
        return self.transaction_reference + " - " + self.clientele_name


p1_main = []
p2_main = []


class PurchaseTransactionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PurchaseTransactionForm, self).__init__(*args, **kwargs)
        clientele_id = Clientele.objects.exclude(clientele_type__icontains='eb-client').values_list("id",
                                                                                                    "clientele_name")
        product_id = Product.objects.all().values_list("id", "product_name")

        p1_main = []
        for i in clientele_id:
            k = list(i)
            k[0] = str(k[0])
            l = (tuple(k))
            p1_main.append(l)
        p1_mains = [('', 'SELECT')] + p1_main
        self.fields['clientele_name'] = ChoiceField(choices=p1_mains, label='Clientele Name')
        p2_main = []
        for i in product_id:
            k = list(i)
            k[0] = str(k[0])
            l = (tuple(k))
            p2_main.append(l)
        p2_mains = [('', 'SELECT')] + p2_main
        self.fields['product_name'] = ChoiceField(choices=p2_mains, label='Product Name')

    class Meta:
        model = PurchaseTransaction
        # fields = '__all__' #to include all the fields in the form

        # specify what fields to be included in the form
        fields = ['date_initiated', 'waybill_number', 'clientele_name', 'product_name', 'product_discount',
                  'product_quantity',
                  'deductions', 'product_rate', 'quantity_value', 'expected_oil', 'expected_cake', 'cake_value',
                  'diesel_litres', 'diesel_rate', 'diesel_value', 'gen_diesel_litres', 'gen_diesel_rate',
                  'gen_diesel_value', 'other_costs', 'transaction_cost',
                  'transaction_income', 'amount_paid']

        widgets = {
            'date_initiated': AdminDateWidget(),
            'waybill_number': NumberInput(attrs={'class': 'form-control'}),
            'product_discount': NumberInput(attrs={'class': 'form-control'}),
            'product_quantity': NumberInput(attrs={'class': 'form-control'}),
            'deductions': NumberInput(attrs={'class': 'form-control'}),
            'product_rate': NumberInput(attrs={'class': 'form-control'}),
            'quantity_value': NumberInput(attrs={'class': 'form-control', 'readOnly': True}),
            'transaction_income': NumberInput(attrs={'class': 'form-control', 'readOnly': True}),
            'expected_oil': NumberInput(attrs={'class': 'form-control', 'readOnly': True}),
            'expected_cake': NumberInput(attrs={'class': 'form-control', 'readOnly': True}),
            'cake_value': NumberInput(attrs={'class': 'form-control', 'readOnly': True}),
            'diesel_litres': NumberInput(attrs={'class': 'form-control'}),
            'diesel_rate': NumberInput(attrs={'class': 'form-control'}),
            'diesel_value': NumberInput(attrs={'class': 'form-control', 'readOnly': True}),
            'gen_diesel_litres': NumberInput(attrs={'class': 'form-control'}),
            'gen_diesel_rate': NumberInput(attrs={'class': 'form-control'}),
            'gen_diesel_value': NumberInput(attrs={'class': 'form-control', 'readOnly': True}),
            'other_costs': NumberInput(attrs={'class': 'form-control'}),
            'transaction_cost': NumberInput(attrs={'class': 'form-control', 'readOnly': True}),
            'amount_paid': NumberInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'date_initiated': _('Date Initiated'),
            'waybill_number': _('Waybill Number'),
            'product_discount': _('Product Discount'),
            'product_quantity': _('Product Quantity (kg)'),
            'product_rate': _('Product Rate'),
            'quantity_value': _('Quantity Value (kg)'),
            'transaction_income': _('Income'),
            'expected_oil': _('Expected Oil'),
            'expected_cake': _('Expected Cake'),
            'cake_value': _('Cake Value'),
            'diesel_litres': _('Diesel Litres'),
            'diesel_rate': _('Diesel Rate'),
            'diesel_value': _('Diesel Value'),
            'gen_diesel_litres': _('Generator Diesel Litres'),
            'gen_diesel_rate': _('Generator Diesel Rate'),
            'gen_diesel_value': _('Generator Diesel Value'),
            'other_costs': _('Other Costs'),
            'transaction_cost': _('Transaction Cost'),
            'amount_paid': _('Amount Paid'),
        }


class SalesTransaction(models.Model):
    date_initiated = models.DateField(max_length=30, null=True)
    transaction_type = models.CharField(max_length=100, null=True)
    transaction_reference = models.CharField(max_length=20, null=True)
    clientele_id = models.IntegerField(null=True, )
    clientele_name = models.CharField(max_length=100)
    product_id = models.IntegerField(null=True)
    product_name = models.CharField(max_length=100)
    narration = models.CharField(max_length=100)
    product_quantity = models.FloatField(null=True)
    product_discount = models.IntegerField(null=True, blank=True)
    product_rate = models.IntegerField(null=True)
    deductions = models.IntegerField(null=True, blank=True)
    quantity_value = models.IntegerField(null=True)
    expected_oil = models.FloatField(null=True, blank=True)
    expected_cake = models.FloatField(null=True, blank=True)
    cake_value = models.FloatField(null=True, blank=True)
    diesel_rate = models.IntegerField(null=True, blank=True)
    diesel_litres = models.IntegerField(null=True, blank=True)
    diesel_value = models.IntegerField(null=True, blank=True)
    gen_diesel_litres = models.IntegerField(null=True, blank=True)
    gen_diesel_rate = models.IntegerField(null=True, blank=True)
    gen_diesel_value = models.IntegerField(null=True, blank=True)
    other_costs = models.FloatField(null=True, blank=True)
    transaction_income = models.IntegerField(null=True)
    transaction_cost = models.IntegerField(null=True)
    waybill_number = models.IntegerField(null=True, blank=True)
    docket_number = models.IntegerField(null=True, blank=True)
    amount_paid = models.IntegerField(null=True, )
    original_approved_date = models.DateTimeField(max_length=30, null=True)
    date_approved = models.DateTimeField(max_length=30, null=True)
    status = models.CharField(max_length=20, null=True)
    initiator = models.CharField(max_length=20, null=True, default="admin")
    updated_by = models.CharField(max_length=20, null=True, default="admin")

    class Meta:
        db_table = "sales_transactions"

    def __str__(self):
        return self.transaction_reference + " - " + self.clientele_name


s_main = []


class SalesTransactionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SalesTransactionForm, self).__init__(*args, **kwargs)
        clientele_id = Clientele.objects.exclude(clientele_type__icontains='eb-client').values_list("id",
                                                                                                    "clientele_name")
        product_id = Product.objects.all().values_list("id", "product_name")

        s1_main = []
        for i in clientele_id:
            k = list(i)
            k[0] = str(k[0])
            l = (tuple(k))
            s1_main.append(l)
        s1_mains = [('', 'SELECT')] + s1_main
        self.fields['clientele_name'] = ChoiceField(choices=s1_mains, label='Clientele Name')
        s2_main = []
        for i in product_id:
            k = list(i)
            k[0] = str(k[0])
            l = (tuple(k))
            s2_main.append(l)
        s2_mains = [('', 'SELECT')] + s2_main
        self.fields['product_name'] = ChoiceField(choices=s2_mains, label='Product Name')

    class Meta:
        model = SalesTransaction
        # fields = '__all__' #to include all the fields in the form

        # specify what fields to be included in the form
        fields = ['date_initiated', 'waybill_number', 'clientele_name', 'product_name', 'product_discount',
                  'product_quantity',
                  'deductions', 'product_rate', 'quantity_value', 'expected_oil', 'expected_cake', 'cake_value',
                  'diesel_litres', 'diesel_rate', 'diesel_value', 'gen_diesel_litres', 'gen_diesel_rate',
                  'gen_diesel_value', 'docket_number', 'other_costs', 'transaction_cost',
                  'transaction_income', 'amount_paid']
        widgets = {
            'date_initiated': AdminDateWidget(),
            'waybill_number': NumberInput(attrs={'class': 'form-control'}),
            'product_discount': NumberInput(attrs={'class': 'form-control'}),
            'product_quantity': NumberInput(attrs={'class': 'form-control'}),
            'deductions': NumberInput(attrs={'class': 'form-control'}),
            'product_rate': NumberInput(attrs={'class': 'form-control'}),
            'quantity_value': NumberInput(attrs={'class': 'form-control', 'readOnly': True}),
            'transaction_income': NumberInput(attrs={'class': 'form-control', 'readOnly': True}),
            'expected_oil': NumberInput(attrs={'class': 'form-control', 'readOnly': True}),
            'expected_cake': NumberInput(attrs={'class': 'form-control', 'readOnly': True}),
            'cake_value': NumberInput(attrs={'class': 'form-control', 'readOnly': True}),
            'diesel_litres': NumberInput(attrs={'class': 'form-control'}),
            'diesel_rate': NumberInput(attrs={'class': 'form-control'}),
            'diesel_value': NumberInput(attrs={'class': 'form-control', 'readOnly': True}),
            'gen_diesel_litres': NumberInput(attrs={'class': 'form-control'}),
            'gen_diesel_rate': NumberInput(attrs={'class': 'form-control'}),
            'gen_diesel_value': NumberInput(attrs={'class': 'form-control', 'readOnly': True}),
            'other_costs': NumberInput(attrs={'class': 'form-control'}),
            'transaction_cost': NumberInput(attrs={'class': 'form-control', 'readOnly': True}),
            'docket_number': NumberInput(attrs={'class': 'form-control'}),
            'amount_paid': NumberInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'date_initiated': _('Date Initiated'),
            'waybill_number': _('Waybill Number'),
            'product_discount': _('Product Discount'),
            'product_quantity': _('Product Quantity '),
            'product_rate': _('Product Rate'),
            'quantity_value': _('Quantity Value'),
            'transaction_income': _('Income'),
            'expected_oil': _('Expected Oil'),
            'expected_cake': _('Expected Cake'),
            'cake_value': _('Cake Value'),
            'diesel_litres': _('Diesel Litres'),
            'diesel_rate': _('Diesel Rate'),
            'diesel_value': _('Diesel Value'),
            'gen_diesel_litres': _('Generator Diesel Litres'),
            'gen_diesel_rate': _('Generator Diesel Rate'),
            'gen_diesel_value': _('Generator Diesel Value'),
            'other_costs': _('Other Costs'),
            'transaction_cost': _('Transaction Cost'),
            'amount_paid': _('Amount Paid'),
            'docket_number': _('Docket Number'),
        }


class TransactionRecord(models.Model):
    transaction_reference = models.CharField(max_length=20, null=True)
    clientele_id = models.IntegerField(null=True)
    transaction_type = models.CharField(max_length=20, null=True)
    transaction_status = models.CharField(max_length=20, null=True)
    transaction_amount = models.IntegerField(null=True)
    approved_by = models.CharField(max_length=20, null=True, default='admin')
    transaction_approved_date = models.DateTimeField(max_length=30, null=True, )

    class Meta:
        db_table = "transactions_record"

    def __str__(self):
        return self.transaction_reference
