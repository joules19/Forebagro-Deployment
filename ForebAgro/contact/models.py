from django.db import models
from django.forms import ModelForm, NumberInput, Select, TextInput, Textarea
from django.utils.translation import ugettext_lazy as _


class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(blank=False)
    message = models.TextField(max_length=250)

    class Meta:
        db_table = "contact"

    def __str__(self):
        return self.full_name


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'message']

        widgets = {
            'full_name': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'message': Textarea(attrs={'class': 'form-control',"style": "resize: none"}),
        }

        labels = {
            'full_name': _("Full Name"),
            'email': _("Email"),
            'message': _("Message")
        }
