from django.shortcuts import render
from .models import Wallet, CryptoCurrency, Amount
from decouple import config
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

# Create your views here.

url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
api_key = config('api_key')

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key,
}

def home(request):
    return render(request, 'home.html')

def wallets_index(request):
    wallets = Wallet.objects.all()
    return render(request, 'wallets/index.html', {'wallets': wallets})

def wallets_detail(request, wallet_id):
    wallet = Wallet.objects.get(id=wallet_id)
    # query database for a specific wallet's coins
    wallet_coins = Amount.objects.filter(wallet=wallet_id)
    print(wallet_coins)
    # symbols_arr = []
    coins_arr = []
    for coin in wallet_coins:
        # symbol = coin.crypto.symbol
        # symbols_arr.append(symbol)
        coin_object = {
            'symbol': coin.crypto.symbol,
            'amount': coin.amount,
        }
        coins_arr.append(coin_object)
    print(coins_arr)

    symbols_arr = []
    for coin in coins_arr:
        symbols_arr.append(coin['symbol'])

    symbols = ','.join(symbols_arr)
    print(symbols)
    parameters = {
        'symbol': symbols
    }

    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        data = data['data']
        coins = []
        # for symbol in symbols_arr:
        #     coin_obj = data[symbol][0]
        #     obj = {
        #         'symbol': symbol,
        #         'name': coin_obj['name'],
        #         'last_updated': coin_obj['last_updated'],
        #         'quote': coin_obj['quote']['USD'],
        #     }
        for coin in coins_arr:
            coin_obj = data[coin['symbol']][0]
            obj = {
                'symbol': coin['symbol'],
                'name': coin_obj['name'],
                'amount': coin['amount'],
                'last_updated': coin_obj['last_updated'],
                'quote': coin_obj['quote']['USD'],
            }

            coins.append(obj)
        print(coins)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    coins_not_in_wallet = CryptoCurrency.objects.exclude(id__in=wallet_coins.values_list('crypto'))
    print(coins_not_in_wallet)

    return render(request, 'wallets/detail.html', {
        'wallet': wallet,
        'avail_coins': coins_not_in_wallet,
        'coins': coins,
    })

