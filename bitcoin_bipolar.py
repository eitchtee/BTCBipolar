from twitter import twittar
from bitcoin import valor_btc
from money.money import Money
from money.currency import Currency
import pickle
import random
from datetime import datetime


if __name__ == '__main__':
    try:
        with open('ultimo_valor.db', 'rb') as db:
            ultimo_valor = pickle.load(db)
    except FileNotFoundError:
        print('Rodando pela primeira vez.')
        valor_atual = valor_btc()
        with open('ultimo_valor.db', 'wb') as db:
            pickle.dump(valor_atual, db, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        valor_atual = valor_btc()
        diferenca = round(abs(valor_atual - ultimo_valor), 2)

        if diferenca > random.randrange(50, 600):
            valor_reais = Money(str(valor_atual), Currency.BRL).format('pt_BR')
            hora = datetime.now().strftime('%H:%M')

            if valor_atual > ultimo_valor:
                msg = "Bitcoin subiu :) - {} às {}".format(valor_reais, hora)
                twittar(msg)
            else:
                msg = "Bitcoin caiu :( - {} às {}".format(valor_reais, hora)
                twittar(msg)
        else:
            print('Diferença insignificante para ser postada.')

    with open('ultimo_valor.db', 'wb') as db:
        pickle.dump(valor_atual, db, protocol=pickle.HIGHEST_PROTOCOL)