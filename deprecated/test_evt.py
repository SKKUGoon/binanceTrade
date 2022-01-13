from dbms.Ddbms import LocalDBMethods2
from datetime import datetime


server = LocalDBMethods2('binance.db')
server.conn.execute(
    "Pragma journal_mode=WAL"
)

td = datetime.now()
test_date = td.strftime('%Y%m%d')
test_hour = td.strftime('%H%M%S')
r = [(test_date, test_hour, 'TRX', 'ico_event', 'long', 'upbit'),
     (test_date, test_hour, 'LUNA', 'ico_event', 'long', 'upbit')]

c = ['date', 'time', 'asset', 'strategy_name', 'strategy', 'source']
server.insert_rows(
    table_name='stgyedr',
    col_=c,
    rows_=r
)