from django.contrib import admin
from . import models
from .models import SalesTransaction
# Register your models here.
admin.site.register(models.ForebDebtTransaction)
admin.site.register(models.CustomerDebtTransaction)
admin.site.register(models.PurchaseTransaction)
admin.site.register(models.SalesTransaction)
admin.site.register(models.ExpenseBasedTransaction)

