from .models import Product

def count_product(request):
    numberofrecords = Product.objects.all().count()
    return {
        'count_product': numberofrecords
    }