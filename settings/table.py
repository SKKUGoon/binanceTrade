
# Event Driven Strategy Table

TABLENAME_EVENTDRIVEN = "stgyedr"
TABLE_EVENTDRIVEN = {
    "date": "Varchar(8) NOT NULL",
    "time": "Varchar(6) NOT NULL",
    "asset": "Varchar(20) NOT NULL",
    "strategy_name": "Varchar(20) NOT NULL",
    "strategy": "Varchar(20)",
    "source": "Varchar(20) NOT NULL"
}

# Coin Account Balance
TABLENAME_ACCOUNT = "stgrres"
TABLE_ACCOUNT = {
    "date": "Varchar(8) NOT NULL",
    "time": "Varchar(6) NOT NULL",
    "usdt_asset": "float",
    "state": "Varchar(20)"
}