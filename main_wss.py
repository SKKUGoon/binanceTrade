from binance import ThreadedWebsocketManager, Client
from dateutil.relativedelta import FR, relativedelta
import datetime
import queue
import json


def get_token(target:str, typ:str, loc='key.json') -> str:
    with open(loc, 'r') as file:
        dat = json.load(file)

    file.close()
    return dat[target][typ]


class BinanceLiveStream:
    def __init__(self, ):
        self.id = get_token('binance_live', 'access_key')
        self.pw = get_token('binance_live', 'secret_key')

        self.spot_close = 'init'
        self.q_spread = queue.Queue(maxsize=20)

    def report_futr_tick(self, msg):
        best_bid = msg['data']['b']
        best_ask = msg['data']['a']
        print('swap', best_bid, best_ask)

    def report_deli_tick(self, msg):
        best_bid = msg['data']['b']
        best_ask = msg['data']['a']
        print('deli', best_bid, best_ask)

    def get_future_expr(self, dfmt='%Y%m%d'):
        """
        Binance Future always expires on
        LAST FRIDAY OF THE MONTH.
        """
        expr_month = {
            1: 2, 2: 1, 3: 0,
            4: 2, 5: 1, 6: 0,
            7: 2, 8: 1, 9: 0,
            10: 2, 11: 1, 12: 0
        }
        m = datetime.date.today().month
        last_fri = (
                datetime.date.today() +
                relativedelta(day=31, weekday=FR(-1), months=expr_month[m])
        )
        return f"_{last_fri.strftime(dfmt)[2:]}"

    def main(self, symbol:str):
        twm_kline = ThreadedWebsocketManager(self.id, self.pw)
        twm_tick = ThreadedWebsocketManager(self.id, self.pw)

        twm_kline.start()
        twm_tick.start()

        # TICKER
        expr_month = self.get_future_expr()
        twm_tick.start_symbol_ticker_futures_socket(
            callback=self.report_futr_tick,
            symbol=symbol
        )
        twm_tick.start_symbol_ticker_futures_socket(
            callback=self.report_deli_tick,
            symbol=f'{symbol}{expr_month}'
        )
        print(f'getting deli for ETHUSDT_{expr_month}')
        twm_kline.join()
        twm_tick.join()


if __name__ == '__main__':
    b = BinanceLiveStream()
    b.main('ETHUSDT')