from json.decoder import JSONDecodeError

import requests


def valor_btc(moeda: str = 'BRL'):
    api_link = "https://blockchain.info/ticker"

    request = requests.get(api_link)
    try:
        result_list = request.json()
        valor = result_list[moeda]["last"]
    except JSONDecodeError:
        return None

    return valor
