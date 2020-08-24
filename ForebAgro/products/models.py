from django.db import models
from django.forms import ModelForm, NumberInput, Select, TextInput
from django.utils.translation import ugettext_lazy as _

class Product(models.Model):
    product_name = models.CharField(max_length=100)

    class Meta:
        db_table = "products"

    def __str__(self):
        return self.product_name


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

        widgets = {

            'product_name': TextInput(attrs={'class': 'form-control'}),
        }

        labels = {

            'product_name': _("Product Name"),
        }


