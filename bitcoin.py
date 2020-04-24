import requests


def valor_btc(moeda: str = 'BRL'):
    api_link = "https://blockchain.info/ticker"

    request = requests.get(api_link)
    result_list = request.json()
    valor = result_list[moeda]["last"]

    return valor


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
