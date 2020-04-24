import os
import pickle
import signal
import time
from datetime import datetime

from money.currency import Currency
from money.money import Money

from bitcoin import valor_btc
from twitter import twittar


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


if __name__ == '__main__':
    work_dir = os.path.dirname(os.path.realpath(__file__))
    db_path = os.path.normpath('{}/ultimo_valor.db'.format(work_dir))

    killer = GracefulKiller()
    while not killer.kill_now:
        try:
            with open(db_path, 'rb') as db:
                ultimo_valor = pickle.load(db)
        except FileNotFoundError:
            print('Rodando pela primeira vez.')
            try:
                valor_atual = valor_btc()
            except:
                time.sleep(600)
                continue
            with open(db_path, 'wb') as db:
                pickle.dump(valor_atual, db, protocol=pickle.HIGHEST_PROTOCOL)
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
                            time.sleep(900)
                            continue
                        print(msg)
                    elif ultimo_valor > valor_atual:
                        msg = f"🔴 Bitcoin caiu :( - {valor_reais} às {hora}"
                        try:
                            twittar(msg)
                        except:
                            time.sleep(900)
                            continue
                        print(msg)
                    with open(db_path, 'wb') as db:
                        pickle.dump(valor_atual, db,
                                    protocol=pickle.HIGHEST_PROTOCOL)
                else:
                    print(f'Diferença insignificante para ser postada. Ultimo '
                          f'valor: {ultimo_valor} | Valor a'
                          f'tual: {valor_atual} | Diferença: {diferenca}')
            except:
                time.sleep(900)
                continue
            else:
                time.sleep(450)

    print("Parando execução.")
