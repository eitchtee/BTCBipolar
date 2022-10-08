import requests
from pycoingecko import CoinGeckoAPI


def valor_btc(moeda: str = 'BRL', segunda_moeda="USD"):
    cg = CoinGeckoAPI()
    result = cg.get_price(ids='bitcoin', vs_currencies='{},{}'.format(moeda, segunda_moeda), include_24hr_change='true')
    moeda_valor = result['bitcoin'][moeda.lower()]
    moeda_24_hrs = result['bitcoin']['{}_24h_change'.format(moeda.lower())] / 100

    if segunda_moeda:
        segunda_moeda_valor = result['bitcoin'][segunda_moeda.lower()]
        segunda_moeda_24_hrs = result['bitcoin']['{}_24h_change'.format(segunda_moeda.lower())] / 100

        return moeda_valor, moeda_24_hrs, segunda_moeda_valor, segunda_moeda_24_hrs
    else:
        return moeda_valor, moeda_24_hrs


def bloco_num():
    api_link = "https://blockchain.info/q/getblockcount"

    request = requests.get(api_link, timeout=180)
    result = int(request.text)

    return result


def block_date(block_num):
    api_link = f"https://blockchain.info/rawblock/{block_num}"

    request = requests.get(api_link, timeout=180)
    result = request.json()

    return int(result['time'])
