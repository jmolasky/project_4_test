from django.shortcuts import render
from .models import Wallet, CryptoCurrency, Amount

# Create your views here.

API_URL = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest/'
api_key = '0bbe40e4-ecd1-4154-832e-e94024a5dd46'


def home(request):
    return render(request, 'home.html')

def wallets_index(request):
    wallets = Wallet.objects.all()
    return render(request, 'wallets/index.html', {'wallets': wallets})

def wallets_detail(request, wallet_id):
    wallet = Wallet.objects.get(id=wallet_id)
    # query database for a specific wallet's coins
    wallet_coins = Amount.objects.filter(wallet=wallet_id)
    # TODO: use the API to pull additional data about each currency to display - will need to do some
    # math etc. to get this to work but it should be doable
   
    coins_not_in_wallet = CryptoCurrency.objects.exclude(id__in=wallet_coins.values_list('crypto'))

    return render(request, 'wallets/detail.html', {
        'wallet': wallet,
        'avail_coins': coins_not_in_wallet,
        'coins': wallet_coins,
    })

