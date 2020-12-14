import requests
from pycoingecko import CoinGeckoAPI


def valor_btc(moeda: str = 'BRL', segunda_moeda="USD"):
    cg = CoinGeckoAPI()
    result = cg.get_price(ids='bitcoin', vs_currencies='usd,brl', include_24hr_change='true')

    moeda_valor = result['bitcoin'][moeda.lower()]

    if segunda_moeda:
        segunda_moeda_valor = result['bitcoin'][segunda_moeda.lower()]
        return moeda_valor, segunda_moeda_valor
    else:
        return moeda_valor


def bloco_num():
    api_link = "https://blockchain.info/q/getblockcount"

    request = requests.get(api_link)
    result = int(request.text)

    return result


def block_date(block_num):
    api_link = f"https://blockchain.info/rawblock/{block_num}"

    request = requests.get(api_link)
    result = request.json()

    return int(result['time'])
