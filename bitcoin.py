import requests


def valor_btc(moeda: str = 'BRL', segunda_moeda= "USD"):
    api_link = "https://blockchain.info/ticker"

    request = requests.get(api_link)
    result_list = request.json()
    moeda_valor = result_list[moeda]["last"]

    if segunda_moeda:
        usd_valor = result_list[segunda_moeda]["last"]
        return moeda_valor, usd_valor
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
