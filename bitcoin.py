import requests


def valor_btc(moeda: str = 'BRL'):
    api_link = "https://blockchain.info/ticker"

    request = requests.get(api_link)
    result_list = request.json()
    valor = result_list[moeda]["last"]

    simbolo = result_list[moeda]["symbol"]

    return simbolo, valor
