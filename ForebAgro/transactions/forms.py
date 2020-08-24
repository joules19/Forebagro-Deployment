from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from .models import  TransactionRecord
from clientele.models import Clientele
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, TextInput, CharField, NumberInput, Select, ChoiceField, DateInput
from .models import ExpenseBasedTransactionForm, ExpenseBasedTransaction, TransactionRecord, CustomerDebtTransaction, \
    CustomerDebtTransactionForm, ForebDebtTransactionForm, SalesTransaction, SalesTransactionForm, ForebDebtTransaction, \
    PurchaseTransaction, PurchaseTransactionForm


class SummaryForm(forms.Form):
    start = forms.DateField(widget=AdminDateWidget(), label='Start Date')
    end = forms.DateField(widget=AdminDateWidget(), label='End Date')

    class Meta:
        fields = ('start', 'end')


class CustomerForm(forms.Form):
    name = forms.ChoiceField(label='Clientele Name' )
    start = forms.DateField(widget=AdminDateWidget(), label='Start Date')
    end = forms.DateField(widget=AdminDateWidget(), label='End Date')

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        names = [(c.id, c.clientele_name) for c in Clientele.objects.exclude(clientele_type__icontains='eb-client')]
        self.fields['name'] = ChoiceField(choices=[('', 'SELECT')] + names, label='Clientele Name')

    class Meta:
        fields = ('name', 'start', 'end', )


class PTForm(ModelForm):
    class Meta:
        model = PurchaseTransaction
        # fields = '__all__' #to include all the fields in the form

        # specify what fields to be included in the form
        fields = ['date_initiated', 'clientele_name', 'product_name', 'product_discount', 'product_quantity',
                  'deductions', 'product_rate',  'quantity_value', 'expected_oil', 'expected_cake', 'cake_value',
                  'diesel_litres', 'diesel_rate', 'diesel_value', 'gen_diesel_litres', 'gen_diesel_rate',
                  'gen_diesel_value', 'waybill_number', 'other_costs', 'transaction_cost',
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
            'clientele_name': TextInput(attrs={'class': 'form-control', 'readOnly': True}),
            'product_name': TextInput(attrs={'class': 'form-control', 'readOnly': True}),
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
            'amount_paid': _('Amount To Pay'),
        }

class SLForm(ModelForm):
    class Meta:
        model = SalesTransaction
        # fields = '__all__' #to include all the fields in the form

        # specify what fields to be included in the form
        fields = ['date_initiated', 'clientele_name', 'product_name', 'product_discount', 'product_quantity',
                  'deductions', 'product_rate',  'quantity_value', 'expected_oil', 'expected_cake', 'cake_value',
                  'diesel_litres', 'diesel_rate', 'diesel_value', 'gen_diesel_litres', 'gen_diesel_rate',
                  'gen_diesel_value', 'waybill_number', 'other_costs', 'transaction_cost',
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
            'clientele_name': TextInput(attrs={'class': 'form-control', 'readOnly': True}),
            'product_name': TextInput(attrs={'class': 'form-control', 'readOnly': True}),
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
            'amount_paid': _('Amount To Pay'),
        }

class EBForm(ModelForm):

    class Meta:
        model = ExpenseBasedTransaction
        # fields = '__all__' #to include all the fields in the form

        # specify what fields to be included in the form
        fields = ['date_initiated', 'clientele_name', 'rate',
                  'quantity', 'total_cost']

        widgets = {
            'date_initiated': AdminDateWidget(),
            'rate': NumberInput(attrs={'class': 'form-control',}),
            'quantity': NumberInput(attrs={'class': 'form-control', }),
            'total_cost': NumberInput(attrs={'class': 'form-control', 'readOnly': True}),
            'clientele_name': TextInput(attrs={'class': 'form-control', 'readOnly': True}),
        }

        labels = {
            'date_initiated': _('Date Initiated'),
            'eb_client': _('Expensed-Based Client'),
            'rate': _('Rate'),
            'quantity': _('Quantity'),
            'total_cost': _('Total Cost'),
        }

class CDForm(ModelForm):
    class Meta:
        model = CustomerDebtTransaction
        # fields = '__all__' #to include all the fields in the form

        # specify what fields to be included in the form
        fields = ['clientele_name', 'amount_paid', 'narration', 'comments', 'date_initiated']

        widgets = {
            'amount_paid': NumberInput(attrs={'class': 'form-control'}),
            'narration': Select(attrs={'class': 'form-control'}),
            'comments': TextInput(attrs={'class': 'form-control'}),
            'date_initiated': AdminDateWidget(),
            'clientele_name': TextInput(attrs={'class': 'form-control', 'readOnly': True}),
        }

        labels = {
            'date_initiated': _('Date Initiated'),
            'narration': _('Narration'),
            'comments': _('Comments'),
            'amount_paid': _('Amount Paid'),
            'clientele_name': _('Clientele NAme'),
        }

class FDForm(ModelForm):
    class Meta:
        model = ForebDebtTransaction
        # fields = '__all__' #to include all the fields in the form

        # specify what fields to be included in the form
        fields = ['clientele_name', 'amount_paid', 'narration', 'comments', 'date_initiated']

        widgets = {
            'amount_paid': NumberInput(attrs={'class': 'form-control'}),
            'narration': Select(attrs={'class': 'form-control'}),
            'comments': TextInput(attrs={'class': 'form-control'}),
            'date_initiated': AdminDateWidget(),
            'clientele_name': TextInput(attrs={'class': 'form-control', 'readOnly': True}),
        }

        labels = {
            'date_initiated': _('Date Initiated'),
            'narration': _('Narration'),
            'comments': _('Comments'),
            'amount_paid': _('Amount Paid'),
            'clientele_name': _('Clientele Name'),
        }