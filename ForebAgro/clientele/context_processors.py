from .models import Clientele

def count_creditor(request):
    numberofrecords = Clientele.objects.filter(clientele_wallet_balance__gt=0)[:20].count()
    return {
        'count_creditor': numberofrecords
    }

def count_debtor(request):
    numberofrecords = Clientele.objects.filter(clientele_wallet_balance__lte=-0.9)[:20].count()
    return {
        'count_debtor': numberofrecords
    }