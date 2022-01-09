from binance import ThreadedWebsocketManager
import json

def get_token(target:str, typ:str, loc='key.json') -> str:
    with open(loc, 'r') as file:
        dat = json.load(file)
    file.close()
    return dat[target][typ]


id = get_token('binance_live', 'access_key')
pw = get_token('binance_live', 'secret_key')

twm = ThreadedWebsocketManager(id, pw)
twm.start()

twm.join()