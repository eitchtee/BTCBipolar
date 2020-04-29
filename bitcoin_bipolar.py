import locale
import os
import pickle
import signal
import time
import traceback
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


def checar_diferenca(ultimo_valor, valor_atual):
    valor_minimo = 600
    diferenca = round(abs(valor_atual - ultimo_valor), 2)

    return diferenca > valor_minimo, diferenca, valor_atual > ultimo_valor


def bitcoin_price_check():
    # Carrega o último valor verificado de uma db ou cria a database e
    # aguarda a próxima execução
    try:
        with open(valor_db_path, 'rb') as db:
            ultimo_valor = pickle.load(db)
    except FileNotFoundError:
        print('Rodando pela primeira vez.')
        try:
            valor_atual_brl = valor_btc()
            with open(valor_db_path, 'wb') as db:
                pickle.dump(valor_atual_brl, db,
                            protocol=pickle.HIGHEST_PROTOCOL)
        except:
            traceback.print_exc()
            return
    else:
        try:
            valor_atual_brl, valor_atual_usd = valor_btc()

            dif_check, dif_valor, subiu = checar_diferenca(ultimo_valor,
                                                           valor_atual_brl)

            if dif_check:
                valor_reais = Money(str(valor_atual_brl), Currency.BRL). \
                    format('pt_BR')
                valor_dolar = Money(str(valor_atual_usd), Currency.USD). \
                    format('pt_BR')
                hora = datetime.now().strftime('%H:%M')
                dia = datetime.now().strftime('%d/%m/%Y')

                if subiu:
                    msg = f"🟢 Bitcoin subiu :)\n" \
                          f"🇧🇷 {valor_reais}\n" \
                          f"🇺🇸 {valor_dolar}\n" \
                          f"Em {dia} às {hora}."
                    try:
                        twittar(msg)
                        print(f"🟢 Bitcoin subiu. "
                              f'Último valor: {ultimo_valor} | '
                              f'Valor atual: {valor_atual_brl} | '
                              f'Diferença: {dif_valor}')
                    except:
                        traceback.print_exc()
                        return
                else:
                    msg = f"🔴 Bitcoin caiu :(\n" \
                          f"🇧🇷 {valor_reais}\n" \
                          f"🇺🇸 {valor_dolar}\n" \
                          f"Em {dia} às {hora}."
                    try:
                        twittar(msg)
                        print(f"🔴 Bitcoin caiu. "
                              f'Último valor: {ultimo_valor} | '
                              f'Valor atual: {valor_atual_brl} | '
                              f'Diferença: {dif_valor}')
                    except:
                        traceback.print_exc()
                        return
                with open(valor_db_path, 'wb') as db:
                    pickle.dump(valor_atual_brl, db,
                                protocol=pickle.HIGHEST_PROTOCOL)
            else:
                print(f'Diferença insignificante para ser postada. Último '
                      f'valor: {ultimo_valor} | Valor a'
                      f'tual: {valor_atual_brl} | Diferença: {dif_valor}')
        except:
            traceback.print_exc()
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
            traceback.print_exc()
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
            traceback.print_exc()
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
            print(f'⚠ O Bitcoin Halving de {ano} aconteceu! '
                  f'O bloco {halving_check_num:n} foi criado '
                  f'às {block_hour} de {block_day}.')
        except:
            traceback.print_exc()
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
        print("---")  # Separa os logs de cada execução.
        time.sleep(randint(300, 900))

    print("Parando execução.")
