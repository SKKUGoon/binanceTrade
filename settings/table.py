from dbms.Ddbms import LocalDBMethods


# Event Driven Strategy Table

TABLENAME_STRAT = "LOG_STRATEGY"
TABLE_STRAT = {
    "date": "VARCHAR(20) NOT NULL",
    "time": "VARCHAR(20) NOT NULL",
    "strategy_name": "VARCHAR(20)",
    "symbol": "VARCHAR(20)",
}

# Coin Account Balance
TABLENAME_CLIENT = "LOG_CLIENT"
TABLE_CLIENT = {
    "date": "Varchar(10) NOT NULL",
    "time": "Varchar(10) NOT NULL",
    "module": "Varchar(20) NOT NULL",
    "status": "Varchar(20)"
}


if __name__ == "__main__":
    server = LocalDBMethods(r'../socket_client/TDB.db')
    server.create_table_w_pk(
        table_name=TABLENAME_STRAT,
        variables=TABLE_STRAT,
        pk_loc=[0, 1]
    )
    server.create_table_w_pk(
        table_name=TABLENAME_CLIENT,
        variables=TABLE_CLIENT,
        pk_loc=[0, 1, 2]
    )
