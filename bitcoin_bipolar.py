import locale
import os
import pickle
import signal
import time
from datetime import datetime
from random import randint

from money.currency import Currency
from money.money import Money

from bitcoin import valor_btc, bloco_num, block_date
from twitter import twittar

locale.setlocale(locale.LC_ALL, '')


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


def bitcoin_price_check():
    try:
        with open(valor_db_path, 'rb') as db:
            ultimo_valor = pickle.load(db)
    except FileNotFoundError:
        print('Rodando pela primeira vez.')
        try:
            valor_atual = valor_btc()
            with open(valor_db_path, 'wb') as db:
                pickle.dump(valor_atual, db, protocol=pickle.HIGHEST_PROTOCOL)
        except:
            return
    else:
        try:
            valor_atual = valor_btc()

            diferenca = round(abs(valor_atual - ultimo_valor), 2)

            if diferenca > 600:
                valor_reais = Money(str(valor_atual), Currency.BRL). \
                    format('pt_BR')
                hora = datetime.now().strftime('%H:%M')

                if valor_atual > ultimo_valor:
                    msg = f"🟢 Bitcoin subiu :) - {valor_reais} às {hora}"
                    try:
                        twittar(msg)
                    except:
                        return
                    print(msg)
                elif ultimo_valor > valor_atual:
                    msg = f"🔴 Bitcoin caiu :( - {valor_reais} às {hora}"
                    try:
                        twittar(msg)
                    except:
                        return
                    print(msg)
                with open(valor_db_path, 'wb') as db:
                    pickle.dump(valor_atual, db,
                                protocol=pickle.HIGHEST_PROTOCOL)
            else:
                print(f'Diferença insignificante para ser postada. Ultimo '
                      f'valor: {ultimo_valor} | Valor a'
                      f'tual: {valor_atual} | Diferença: {diferenca}')
        except:
            return


def halving_check():
    try:
        with open(bloco_db_path, 'rb') as db:
            ultimo_bloco = pickle.load(db)
    except FileNotFoundError:
        print('Analisando blocos pela primeira vez.')
        try:
            cur_bloco = bloco_num()
            with open(bloco_db_path, 'wb') as db:
                pickle.dump(cur_bloco, db, protocol=pickle.HIGHEST_PROTOCOL)
        except:
            return

    halving_check_num = 0

    while halving_check_num < ultimo_bloco:
        halving_check_num += 210000

    cur_bloco = bloco_num()
    ano = datetime.now().strftime('%Y')

    if cur_bloco >= halving_check_num > ultimo_bloco:
        try:
            block_creation_stamp = block_date(halving_check_num)
        except:
            print('Não foi possível acessar data do bloco. Tentando na '
                  'próxima ronda.')
            return

        block_creation_date_obj = datetime.fromtimestamp(block_creation_stamp)

        block_day = block_creation_date_obj.strftime('%d/%m')
        block_hour = block_creation_date_obj.strftime('%H:%M')

        msg = f'⚠ O Bitcoin Halving de {ano} aconteceu!\n' \
              f'O bloco {halving_check_num:n} foi criado ' \
              f'às {block_hour} de {block_day}.'
        try:
            twittar(msg)
        except:
            return
    else:
        print(f"Halving ainda não aconteceu. Bloco atual: {cur_bloco} | "
              f"Halving em: {halving_check_num} | "
              f"Faltam: {halving_check_num - cur_bloco}")

    with open(bloco_db_path, 'wb') as db:
        pickle.dump(cur_bloco, db,
                    protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    work_dir = os.path.dirname(os.path.realpath(__file__))
    valor_db_path = os.path.normpath('{}/ultimo_valor.db'.format(work_dir))
    bloco_db_path = os.path.normpath('{}/ultimo_bloco.db'.format(work_dir))

    killer = GracefulKiller()
    while not killer.kill_now:
        bitcoin_price_check()
        halving_check()
        print()
        time.sleep(randint(300, 900))

    print("Parando execução.")
