from import_export import resources
from .models import SalesTransaction, PurchaseTransaction

class SalesResource(resources.ModelResource):
    class Meta:
        model = SalesTransaction

