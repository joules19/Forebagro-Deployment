from django.db import models
from django.forms import ModelForm, NumberInput, Select, TextInput
from django.utils.translation import ugettext_lazy as _

class Constants(models.Model):
    constant_name = models.CharField(max_length=100, unique=True)
    constant_value = models.FloatField( null=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    date_updated = models.DateField(max_length=100, null=True)
    updated_by = models.CharField(max_length=100, null=True)


    class Meta:
        db_table = "constant"

    def __str__(self):
        return self.constant_name


class ConstantsForm(ModelForm):
    class Meta:
        model = Constants
        fields = ['constant_name', 'constant_value', 'description']

        widgets = {

            'constant_name': TextInput(attrs={'class': 'form-control'}),
            'constant_value': NumberInput(attrs={'class': 'form-control'}),
            'description': TextInput(attrs={'class': 'form-control'}),
        }

        labels = {

            'constant_name': _("Constant Name"),
            'constant_value': _("Constant Value"),
        }


