from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, TextInput, CharField, NumberInput, Select, PasswordInput, ChoiceField
from django.core.validators import MinLengthValidator


# Create your models here.
class Clientele(models.Model):

    clientele_name = models.CharField(max_length=100, unique=True, null=False, help_text="Clientele Name")
    clientele_type = models.CharField(max_length=20, )
    clientele_address = models.CharField(max_length=20, null=True, blank=True)
    clientele_contact_number = models.CharField(max_length=20, blank=True)
    clientele_email = models.EmailField(blank=True)
    clientele_wallet_balance = models.FloatField(max_length=20, null=True, blank=True)
    default_wallet_balance = models.FloatField(default=0, null=True)

    class Meta:
        db_table = "clientele"
        ordering = ('clientele_name',)

    def __str__(self):
        return self.clientele_name


class ClienteleForm(ModelForm):


    class Meta:

        clientele_type = [('', 'SELECT'), ('supplier', 'Supplier'), ('buyer', 'Buyer'), ('both', 'Both'),
                          ('eb-client', 'Expense-Based Client')]
        model = Clientele
        # fields = '__all__' #to include all the fields in the form

        # specify what fields to be included in the form
        fields = ['clientele_name', 'clientele_type', 'clientele_address', 'clientele_email',
                  'clientele_contact_number']

        widgets = {
            'clientele_name': TextInput(attrs={'class': 'form-control'}),
            'clientele_type': Select(attrs={'class': 'form-control'},choices=clientele_type),
            'clientele_address': TextInput(attrs={'class': 'form-control'}),
            'clientele_email': TextInput(attrs={'class': 'form-control'}),
            'clientele_contact_number': NumberInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'clientele_name': _("Clientele Name"),
            'clientele_contact_number': _("Contact Number"),
            'clientele_email': _("Clientele Email"),
            'clientele_wallet_balance': _("Clientele Wallet Balance"),
            'clientele_address': _("Clientele Address"),
            'clientele_type': _("Clientele Type"),
        }

        # help_text ={
        # 	'dealer_name':_("Input the correct dealer name"),
        # 	'dealer_contact_number':_("Contact number must a Globe network"),
        # }

        error_message = {
            'dealer_address': {
                'max_length': _("Address must not exceed 20 characters"),
            }
        }

    # validators = {
    # 	'dealer_address': MinLengthValidator(2)
    # }
